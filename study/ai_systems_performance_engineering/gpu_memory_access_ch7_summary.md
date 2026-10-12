# Chapter 7. Profiling and Tuning GPU Memory Access Patterns

## 챕터 개요

모델이 커질수록 이론적인 연산 성능과 실제 성능 사이의 차이를 만드는 주요 원인 중 하나는 **메모리 시스템**이다. 이 장은 GPU 커널이 메모리에 접근하는 방식을 최적화해 낭비되는 대역폭을 줄이고, 데이터 재사용을 늘리는 방법을 다룬다.

핵심 기법:

- Coalescing
- Vectorized load/store
- Shared memory tiling
- Shared-memory bank conflict 회피
- Warp shuffle
- Read-only data cache
- 비동기 prefetch와 TMA(Tensor Memory Accelerator)

**목표:** 메모리 접근 낭비를 줄이고 arithmetic intensity를 높여, 커널의 병목을 memory-bound에서 compute-bound 쪽으로 이동시키는 것.

### 핵심 용어

- **HBM(High Bandwidth Memory):** GPU에 연결된 고대역폭 메모리. GPU 관점에서 HBM은 DRAM의 한 종류다.
- **DMA(Direct Memory Access):** CPU/GPU 연산 유닛이 직접 데이터를 복사하는 대신, 하드웨어 엔진이 메모리 사이의 데이터 이동을 담당하는 방식.
- **TMA(Tensor Memory Accelerator):** Hopper부터 도입된 global memory와 shared memory 사이의 대량 복사를 위한 전용 엔진.
- **Cache line:** 캐시가 다루는 메모리 구간. 이 장의 예시에서는 128바이트 단위로 설명한다.
- **Sector:** cache line을 구성하는 32바이트 조각. 예시 기준 cache line 하나는 sector 4개로 구성된다.
- **Arithmetic intensity:** 메모리에서 옮긴 바이트당 수행한 연산 수(FLOP/byte).

---

## 7-1. Coalesced vs. Uncoalesced Global Memory Access

### 기본 용어

- **Thread:** GPU에서 커널 코드를 실행하는 가장 작은 실행 단위.
- **Warp:** 32개 thread의 묶음. 같은 warp의 thread들은 같은 명령을 실행하며, 각자 다른 데이터 주소를 다룰 수 있다.
- **Global memory:** GPU 칩 바깥의 메인 메모리. 예를 들어 Blackwell GPU에서는 HBM3e를 사용하며, 용량은 크지만 접근 지연이 길다.
- **Memory transaction:** 하드웨어가 global memory와 데이터를 주고받는 단위 요청.
- **Cache line:** 메모리 시스템이 다루는 128바이트 단위 구간.
- **Sector:** cache line 안의 32바이트 조각. 실제 접근은 필요한 sector 단위로 처리될 수 있다.

### Coalescing이란?

warp가 load 명령을 실행하면 32개 thread가 각각 메모리 주소를 요청한다. 하드웨어는 이 요청들을 개별적으로 처리하는 대신, 주소들이 어느 cache line과 sector에 속하는지 확인하고 가능한 한 적은 수의 트랜잭션으로 묶는다.

이처럼 **warp 내 여러 thread의 메모리 요청을 적은 수의 트랜잭션으로 합치는 동작**을 coalescing이라고 한다.

Coalescing 효율은 32개 thread의 주소가 얼마나 **연속적이고 정렬되어 있는지**에 영향을 받는다.

### Coalesced 접근: 이상적인 경우

조건:
- thread `i`가 `in[i]`를 읽는다.
- 인접 thread가 인접한 메모리 주소를 읽는다.
- 시작 주소가 128바이트 경계에 정렬되어 있다.

float가 4바이트라면:

- 32 threads × 4바이트 = 128바이트
- 128바이트 구간은 cache line 하나, sector 네 개에 해당한다.
- 가져온 데이터 대부분을 실제로 사용하므로 낭비가 적다.

```cpp
int idx = blockIdx.x * blockDim.x + threadIdx.x;
out[idx] = in[idx];  // 인접 thread가 인접 원소에 접근
```

### Uncoalesced 접근

#### ① Strided access

thread `i`가 `in[i * stride]`를 읽는 경우다.

`stride = 2`이고 float가 4바이트라면 주소는 다음처럼 떨어진다.

- thread 0: 0바이트
- thread 1: 8바이트
- thread 2: 16바이트
- ...
- thread 31: 248바이트

warp가 접근하는 범위는 256바이트이고, 실제 필요한 데이터는 128바이트다. 이 예시에서는 가져온 데이터 중 일부가 사용되지 않는다. stride가 커질수록 주소가 더 많은 sector에 흩어질 수 있고, 최악의 경우 thread마다 서로 다른 sector를 요구할 수 있다.

#### ② Misaligned access

주소는 연속적이지만 시작 주소가 필요한 경계에 맞지 않는 경우다.

예를 들어 4바이트 위치에서 128바이트를 읽으면 4~131바이트 범위를 다루게 된다. 이 접근은 128바이트 경계에 정렬된 경우보다 더 많은 sector에 걸칠 수 있다.

#### ③ Random access

각 thread가 서로 관계없는 주소를 읽는 경우다. 예를 들어 인덱스 배열을 이용해 원소를 골라 읽는 gather 연산이 있다. 주소가 여러 cache line과 sector에 흩어지면 필요한 트랜잭션 수가 늘어날 수 있다.

### 프로파일링에서 확인할 지표

| 지표 | 의미 | 효율적인 접근 | 비효율적인 접근 |
|---|---|---|---|
| Global Memory Load Efficiency | 가져온 바이트 중 실제 사용된 비율 | 높음 | 낮음 |
| Average sectors per request | load 요청당 평균 sector 수 | 4바이트 load 예시에서 약 4가 최적 | 4 초과 가능 |
| DRAM throughput (% of peak) | 최대 메모리 대역폭 대비 사용률 | 병목에 따라 높을 수 있음 | 낮으면서 stall이 많을 수 있음 |

Nsight Compute의 Memory Workload Analysis에서 다음 증상을 살펴볼 수 있다.

- Global Memory Load Efficiency가 낮음
- DRAM sector read 수가 많음
- Average sectors per request가 높음
- DRAM throughput이 낮은데 warp가 메모리 대기로 stall됨

**개선 방향:** 인접한 thread가 인접한 원소를 읽도록 인덱싱하고, 데이터 레이아웃을 점검한다.

### AoS와 SoA

- **AoS(Array of Structures):** `{x, y, z}` 같은 구조체를 배열로 배치한다.
- **SoA(Structure of Arrays):** `x[]`, `y[]`, `z[]`처럼 필드별 배열을 따로 둔다.

커널이 같은 필드의 값을 여러 thread에서 연속적으로 읽는다면 SoA가 더 연속적인 접근을 만들기 쉬울 수 있다. 실제 성능은 커널의 접근 패턴에 따라 달라진다.

비효율적인 예:

```cpp
__global__ void uncoalescedCopy(
    const float* __restrict__ in,
    float* __restrict__ out,
    int N,
    int stride
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        out[idx] = in[idx * stride];
    }
}
```

연속 접근 예:

```cpp
__global__ void coalescedCopy(
    const float* __restrict__ in,
    float* __restrict__ out,
    int N
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        out[idx] = in[idx];
    }
}
```

---

## 7-2. Vectorized Memory Access

### 기본 용어

- **Instruction:** GPU가 실행하는 명령 하나. 메모리에서 읽는 명령은 load, 쓰는 명령은 store다.
- **Scalar load:** thread 하나가 load 명령 하나로 원소 하나를 읽는다. 예를 들어 float 하나는 4바이트다.
- **Vector load:** thread 하나가 load 명령 하나로 연속된 원소 여러 개를 읽는다. 예를 들어 float4는 16바이트다.
- **Alignment:** 데이터 시작 주소가 특정 바이트 수의 배수인 상태. 16바이트 정렬은 시작 주소가 16의 배수인 경우다.
- **PTX(Parallel Thread Execution):** NVIDIA GPU용 중간 단계 명령어 집합. 예를 들어 `ld.global.v4.f32`는 float 4개를 vector load하는 명령을 나타낸다.

### Coalescing과 vectorizing의 차이

- **Coalescing:** 실행 중 warp 안의 여러 thread가 낸 메모리 요청을 하드웨어가 묶는다. thread 사이(interthread)의 최적화다.
- **Vectorizing:** thread 하나가 여러 원소를 한 load/store 명령으로 처리하도록 만든다. thread 내부(intrathread)의 최적화다.

둘은 별개의 최적화이며 함께 사용할 수 있다.

- Coalescing은 필요한 sector와 트랜잭션 낭비를 줄이는 데 초점을 둔다.
- Vectorizing은 같은 양의 데이터를 옮길 때 필요한 load/store 명령 수를 줄이는 데 초점을 둔다.

예를 들어 thread 하나가 float 하나씩 네 번 읽는 대신, 정렬 조건을 만족한 상태에서 float 네 개를 한 번에 읽으면 명령 수를 줄일 수 있다.

### Alignment가 중요한 이유

vector load는 읽기 시작 주소가 vector 크기에 맞게 정렬되어야 한다.

- float4(16바이트): 시작 주소가 16의 배수여야 한다.
- 32바이트 vector: 시작 주소가 32의 배수여야 한다.

`cudaMalloc`은 반환 포인터에 대해 최소 256바이트 정렬을 보장하므로 할당 시작점은 16바이트 및 32바이트 정렬 조건을 만족한다. 다만 포인터에 오프셋을 더하거나 데이터의 실제 배치가 달라지면 접근 주소의 정렬을 별도로 확인해야 한다.

### Blackwell의 32바이트 vector load

원문에서 다루는 하드웨어 기준:

- Hopper까지: thread당 최대 16바이트(128-bit) vector load
- Blackwell + CUDA 13 이후: thread당 32바이트(256-bit) load/store 지원
- 관련 PTX 예시: `ld.global.v8.f32`, `st.global.v8.f32`

32바이트 vector load가 사용되려면 컴파일러가 32바이트 정렬을 증명할 수 있어야 한다. 증명하지 못하면 더 작은 명령 여러 개로 나뉠 수 있다.

```cpp
struct alignas(32) float8 {
    float v[8];
};
```

32개 thread가 thread당 32바이트를 읽는다면 총 1,024바이트를 읽는다. 하드웨어의 메모리 트랜잭션과 sector 처리는 여전히 해당 GPU 메모리 시스템의 단위에 따라 이루어진다. Vector 크기가 커졌다고 해서 실제로 필요한 데이터 양 자체가 줄어드는 것은 아니다.

### PyTorch 예시: 원소별 복사와 텐서 단위 복사

비효율적인 예:

```python
def copy_scalar(inp: torch.Tensor) -> torch.Tensor:
    out = torch.empty_like(inp)
    flat_in, flat_out = inp.view(-1), out.view(-1)

    for i in range(flat_in.numel()):
        flat_out[i] = flat_in[i]

    return out
```

느린 이유:
- 반복문은 CPU에서 Python으로 실행된다.
- 원소별 인덱싱과 대입은 많은 작은 작업과 GPU 작업 호출을 유발할 수 있다.
- 원소가 약 1백만 개라면 작업 호출 오버헤드가 커질 수 있다.

전체 텐서를 한 번에 처리하는 예:

```python
def copy_vectorized(inp: torch.Tensor) -> torch.Tensor:
    vec = inp.view(-1, 4)   # shape만 변경하며 데이터 복사는 하지 않음
    out_vec = vec.clone()   # 전체 텐서를 한 번에 복사
    return out_vec.view(-1)
```

연속 텐서의 `clone()`은 최적화된 device-to-device 복사 경로를 사용할 수 있다. 핵심은 Python에서 원소마다 작업을 요청하는 대신, 전체 텐서 작업을 한 번에 요청해 작은 작업들의 호출 오버헤드를 줄이는 것이다.

---

## 7-3. Tiling and Data Reuse Using Shared Memory

### 기본 용어

- **Thread block:** 여러 thread의 묶음. 한 block의 thread는 같은 SM에서 실행되며 shared memory를 공유할 수 있다.
- **Shared memory:** SM 안에 있는 작고 빠른 on-chip 메모리. 같은 block의 thread들이 함께 읽고 쓸 수 있다.
- **`__shared__`:** 변수를 shared memory에 할당하도록 지정하는 CUDA 키워드.
- **`__syncthreads()`:** block 안의 thread들이 해당 지점에 도달할 때까지 기다리는 barrier.
- **Tile:** 큰 행렬을 나눈 작은 부분 행렬.
- **Arithmetic intensity:** 메모리에서 옮긴 바이트당 수행한 연산 수(FLOP/byte).

### 왜 tiling을 사용하는가?

Naive 행렬곱은 같은 데이터를 global memory에서 여러 번 읽을 수 있다. 예를 들어 각 출력 원소를 계산하는 과정에서 A와 B의 값이 반복적으로 필요해진다.

**Tiling**은 A와 B의 작은 부분 행렬을 shared memory에 올린 뒤, block의 thread들이 그 데이터를 여러 번 재사용하도록 한다.

일반적인 흐름:

1. block이 global memory에서 tile을 읽는다.
2. `__syncthreads()`로 tile 로드가 끝날 때까지 기다린다.
3. shared memory에 저장된 tile을 반복해서 사용해 계산한다.
4. 다음 tile을 덮어쓰기 전에 다시 동기화한다.

이렇게 하면 global memory에서 같은 데이터를 반복해서 읽는 일을 줄이고 arithmetic intensity를 높일 수 있다.

### Naive 행렬곱

```cpp
__global__ void naiveMatMul(
    const float* A,
    const float* B,
    float* C,
    int N
) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < N; ++k) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}
```

### Shared-memory tiling 행렬곱

```cpp
#define TILE_SIZE 32

__global__ void tiledMatMul(
    const float* A,
    const float* B,
    float* C,
    int N
) {
    __shared__ float sA[TILE_SIZE][TILE_SIZE];
    __shared__ float sB[TILE_SIZE][TILE_SIZE];

    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;
    float sum = 0.0f;

    for (int t = 0; t < N; t += TILE_SIZE) {
        sA[threadIdx.y][threadIdx.x] =
            (row < N && t + threadIdx.x < N)
            ? A[row * N + t + threadIdx.x] : 0.0f;

        sB[threadIdx.y][threadIdx.x] =
            (t + threadIdx.y < N && col < N)
            ? B[(t + threadIdx.y) * N + col] : 0.0f;

        __syncthreads();

        for (int k = 0; k < TILE_SIZE; ++k) {
            sum += sA[threadIdx.y][k] * sB[k][threadIdx.x];
        }

        __syncthreads();
    }

    if (row < N && col < N) {
        C[row * N + col] = sum;
    }
}
```

이 예시는 개념 설명용이다. 실제 커널에서는 행렬 크기, tile 크기, 메모리 접근 패턴, 동기화 비용과 하드웨어 특성을 고려해 튜닝해야 한다.

---

## 7-4. Avoid Shared-Memory Bank Conflicts

### Bank와 bank conflict

Shared memory는 여러 **bank**로 나뉘어 있어 서로 다른 bank에 대한 접근을 병렬로 처리할 수 있다.

이 장의 예시에서는:
- bank는 32개다.
- bank 하나는 한 사이클에 4바이트(word) 단위 접근 하나를 처리한다고 설명한다.
- float 배열에서는 bank 번호를 다음처럼 생각할 수 있다.

\[
bank = \left(\frac{\text{byte address}}{4}\right) \bmod 32
\]

따라서 연속된 float 배열의 인덱스를 기준으로 하면 `bank = index % 32`다.

- **Bank conflict:** 같은 warp의 여러 thread가 같은 bank의 서로 다른 주소에 동시에 접근하는 것.
- **N-way bank conflict:** 같은 bank에 N개의 서로 다른 주소 접근이 몰려 여러 차례로 나뉘어 처리되는 경우.
- **Broadcast:** 여러 thread가 같은 주소를 읽는 경우. 하나의 값을 여러 thread에 전달할 수 있으므로 일반적인 bank conflict와 다르다.

서로 다른 bank에 접근하면 병렬 처리할 수 있지만, 같은 bank의 서로 다른 주소에 접근하면 직렬화가 발생해 shared memory의 이점을 줄일 수 있다.

### 대표 사례: 32×32 tile의 열 방향 접근

```cpp
__shared__ float tile[32][32];
float v = tile[threadIdx.x][c];
```

행렬의 원소 인덱스는 `r * 32 + c`다.

```text
bank = (r * 32 + c) % 32
     = c
```

`c`가 고정되어 있고 `r`만 달라지면 모든 thread가 같은 bank에 접근한다. 행 사이 간격이 32 float, 즉 128바이트라 bank 번호가 반복되는 것이다. 이 패턴은 행렬 전치처럼 행 방향으로 쓰고 열 방향으로 읽을 때 나타날 수 있다.

### 해결 방법 1: Padding

행 길이를 32에서 33으로 늘린다.

```cpp
__shared__ float tile[32][33];
float v = tile[threadIdx.x][c];
```

이때 인덱스는 `r * 33 + c`이므로:

```text
bank = (r * 33 + c) % 32
     = (r + c) % 32
```

`r`이 바뀌면 bank도 달라져 충돌을 피할 수 있다.

- 장점: 구현이 단순하다.
- 비용: 추가 shared memory를 사용한다. 32×32 float tile 기준으로 한 행의 float 하나만큼, 총 128바이트가 추가된다.

### 해결 방법 2: Swizzling

주소의 배치를 XOR 같은 규칙으로 재배치한다.

```cpp
// 개념 예시: 저장과 읽기에서 동일한 매핑을 적용
tile[r][c ^ r] = value;
float v = tile[r][c ^ r];
```

- 장점: padding처럼 추가 배열 공간을 쓰지 않고 bank 배치를 바꿀 수 있다.
- 단점: 인덱스 계산과 데이터 매핑이 복잡해진다.
- CUTLASS 같은 고성능 라이브러리에서도 swizzling 계열 기법을 활용한다.

---

## 7-5. Warp Shuffle Intrinsics

### 기본 용어

- **Lane:** warp 안에서 thread의 번호. 보통 0~31 범위다.
- **Register:** 각 thread가 개별적으로 사용하는 매우 빠른 저장 공간. 기본적으로 다른 thread의 register를 직접 읽을 수 없다.
- **Intrinsic:** 컴파일러가 특정 하드웨어 명령으로 변환하는 내장 함수.
- **Warp shuffle:** 같은 warp 안의 thread끼리 register 값을 직접 주고받는 명령.
- **Mask:** shuffle에 참여하는 lane을 나타내는 비트 마스크. `0xffffffff`는 32개 lane 전체를 나타내는 대표적인 값이다.
- **Reduction:** 여러 값을 합계나 최댓값처럼 하나의 값으로 합치는 연산.

### Shared memory 방식의 비용

다른 thread의 register 값을 사용하려면 전통적으로 다음 단계를 거칠 수 있다.

1. 각 thread가 자신의 값을 shared memory에 쓴다.
2. `__syncthreads()`로 쓰기 완료를 기다린다.
3. 다른 thread가 shared memory에서 값을 읽는다.

이 과정에는 shared memory 읽기/쓰기, barrier 비용, 경우에 따른 bank conflict가 발생할 수 있다.

### Warp shuffle로 줄이기

같은 warp 안에서 값을 교환할 수 있다면 warp shuffle을 이용해 shared memory를 거치지 않고 register 값을 직접 전달할 수 있다.

- shared memory 접근을 줄인다.
- 이 경로에서 shared-memory bank conflict가 발생하지 않는다.
- warp 내부 데이터 교환만 필요하다면 block 전체를 대상으로 하는 `__syncthreads()`를 피할 수 있다.

단, shuffle의 유효성은 참여하는 lane과 실행 조건에 따라 달라지므로 mask와 lane 참여 조건을 올바르게 설정해야 한다.

---

## 7-6. Read-Only Data Cache

### 기본 용어

- **Read-only data:** 커널 실행 중 값이 바뀌지 않는 데이터. 예: embedding table, 계수 테이블, lookup table.
- **Read-only data cache:** 읽기 전용 데이터에 적합한 캐시 경로. Volta 이후에는 L1 및 texture cache와 하드웨어를 공유한다.
- **Non-coherent load:** 해당 데이터가 커널 실행 중 바뀌지 않는다는 가정 아래 일관성 확인을 생략하는 load 경로.
- **Aliasing:** 서로 다른 포인터가 같은 메모리 영역을 가리키는 상태.
- **`const`:** 해당 포인터를 통해 값을 쓰지 않겠다는 선언.
- **`__restrict__`:** 포인터가 가리키는 메모리가 다른 관련 포인터와 겹치지 않는다는 점을 컴파일러에 알려주는 선언.
- **`__ldg()`:** read-only 경로로 load하도록 지정하는 CUDA intrinsic.

### 왜 필요한가?

여러 thread가 같은 읽기 전용 데이터를 반복해서 읽는 커널을 생각해 보자. 컴파일러가 데이터가 커널 실행 중 바뀌지 않는다는 사실을 확신하지 못하면, 다른 포인터를 통한 쓰기 가능성을 고려해야 한다. 그 결과 읽기 전용 데이터에 적합한 load 경로를 선택하지 못할 수 있다.

### 최적화 방향

포인터의 사용 조건을 정확히 표현한다.

- `const`: 이 포인터를 통한 쓰기가 없음을 표현한다.
- `__restrict__`: 다른 포인터와 메모리가 겹치지 않음을 표현한다.

두 조건이 실제 코드의 동작과 일치하면 컴파일러가 더 적절한 load 최적화를 적용할 수 있다. **`__restrict__`는 실제로 aliasing이 없을 때만 사용해야 한다.**

```cpp
// Before
__global__ void lookupNaive(
    const float* table,
    float* out,
    int N
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        out[idx] = table[idx % 1024];
    }
}

// After: 포인터의 aliasing 조건을 명시
__global__ void lookupReadOnly(
    const float* __restrict__ table,
    float* __restrict__ out,
    int N
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        out[idx] = table[idx % 1024];
    }
}
```

커널 본문은 같고 포인터 선언이 달라졌다. 컴파일러는 이 정보를 바탕으로 최적화를 더 잘 수행할 수 있다. `const`와 `__restrict__`를 붙였다고 언제나 성능이 향상되는 것은 아니며, 실제 생성 코드와 프로파일링 결과를 확인해야 한다.

---

## 7-7. Asynchronous Memory Prefetching and Tensor Memory Accelerator

### 기본 용어

- **Synchronous load:** load 명령을 실행한 thread가 데이터가 준비될 때까지 기다려야 다음 작업을 진행할 수 있는 방식.
- **Asynchronous copy:** 복사를 요청한 뒤 다른 작업을 진행하고, 데이터가 필요해지는 시점에 완료 여부를 확인하는 방식.
- **Prefetch:** 실제 계산에 필요해지기 전에 데이터를 미리 가져오는 것.
- **LD/ST unit:** SM 안에서 load/store 명령을 처리하는 하드웨어.
- **DMA engine:** 데이터 이동을 전담하는 하드웨어 엔진.
- **TMA(Tensor Memory Accelerator):** Hopper(sm_90)부터 도입된 global memory와 shared memory 사이의 대량 tensor 복사를 담당하는 엔진.
- **Double buffering:** shared memory 버퍼 두 개를 번갈아 사용해, 한 버퍼로 계산하는 동안 다른 버퍼에 다음 데이터를 받는 방식. Ping-pong buffering이라고도 한다.
- **Pipeline stage:** 동시에 진행 중일 수 있는 복사/계산 단계. Double buffering은 두 버퍼를 활용하는 대표적인 2-stage 방식이다.
- **Producer / consumer:** 버퍼를 채우는 쪽 / 버퍼의 데이터를 사용하는 쪽.

### 문제: 복사와 계산이 순차적으로 진행됨

Coalesced load를 사용하더라도 global memory 왕복에는 긴 지연이 발생할 수 있다. 단순한 타일 처리에서는 다음과 같은 순서가 된다.

```text
Tile load
   ↓ (데이터를 기다림)
Tile compute
   ↓
다음 tile load
   ↓
다음 tile compute
```

데이터를 기다리는 동안 연산 유닛이 놀게 되면 warp stall이 발생할 수 있다. 일반적인 load는 thread들이 load 명령을 발행해야 하므로 LD/ST unit과 명령 발행 슬롯을 사용하고, 데이터가 register를 거쳐 shared memory에 들어가는 경로에서는 register 사용도 발생한다.

### 해결 1: 비동기 복사로 계산과 겹치기

다음 tile의 복사를 먼저 요청하고, 복사가 진행되는 동안 현재 tile을 계산한다.

```text
시간 ───────────────────────────────→

복사:   [Tile 0] [Tile 1] [Tile 2]
계산:            [Tile 0] [Tile 1] [Tile 2]
```

계산 시간이 복사 시간과 비슷하거나 더 길면 복사 지연의 일부를 계산 시간 뒤에 숨길 수 있다. 실제로 얼마나 겹칠 수 있는지는 커널과 하드웨어의 조건에 달려 있다.

### 해결 2: Double buffering

복사 중인 버퍼와 계산 중인 버퍼를 분리한다. 같은 버퍼를 동시에 사용하면 아직 읽는 중인 데이터를 덮어쓸 수 있으므로 버퍼 두 개를 번갈아 사용한다.

```text
buffer[0]: Tile 0 계산 → Tile 2 복사 → Tile 2 계산
buffer[1]: Tile 1 복사 → Tile 1 계산 → Tile 3 복사
```

원문에서 설명하는 인덱싱 방식은 다음과 같다.

```cpp
buffer_index = tile_index % 2;
```

짝수 tile은 버퍼 0, 홀수 tile은 버퍼 1을 사용한다. 실제 구현에서는 복사 완료와 계산 완료를 확인하는 동기화도 정확히 관리해야 한다.

### 해결 3: TMA에 복사를 맡기기

TMA는 global memory에서 shared memory로 대량 데이터를 옮기는 작업을 전용 하드웨어에 맡긴다.

- thread는 복사할 영역과 목적지를 지정해 요청한다.
- 데이터 이동을 thread별 load 명령으로 처리하는 부담을 줄인다.
- 원문에서 설명하는 경로에서는 데이터가 thread의 register를 거치지 않고 shared memory로 들어간다.
- 1D~5D tensor 복사와 stride가 있는 영역 복사를 지원한다.

TMA를 활용하면 SM의 LD/ST 명령 발행 부담을 줄이고, thread가 계산에 더 많은 자원을 사용할 수 있다. 다만 TMA를 사용한다고 동기화가 사라지는 것은 아니며, 데이터가 준비된 시점과 버퍼를 재사용하는 시점을 관리해야 한다.

---

## 핵심 내용 요약

| 기법 | 해결하려는 문제 | 핵심 아이디어 |
|---|---|---|
| Coalescing | warp의 메모리 요청이 여러 sector로 흩어짐 | 인접 thread가 인접 주소를 읽게 한다 |
| Vectorized load/store | 같은 데이터를 옮기는 load/store 명령이 많음 | thread 하나가 연속된 여러 원소를 한 명령으로 처리한다 |
| Shared-memory tiling | global memory에서 같은 데이터를 반복해서 읽음 | tile을 shared memory에 올려 block 내에서 재사용한다 |
| Bank-conflict 회피 | shared-memory 접근이 직렬화됨 | padding 또는 swizzling으로 bank 배치를 바꾼다 |
| Warp shuffle | thread 간 값 교환에 shared memory와 barrier가 필요함 | 같은 warp 안에서 register 값을 직접 교환한다 |
| Read-only cache 최적화 | 변경되지 않는 데이터를 읽을 때 최적화 정보가 부족함 | 실제 데이터 조건에 맞게 `const`와 `__restrict__`를 표현한다 |
| Async prefetch / double buffering | 데이터 복사를 기다리며 연산 유닛이 놀음 | 복사와 계산을 겹친다 |
| TMA | thread가 많은 load/store 명령으로 데이터를 옮김 | 대량 복사를 전용 하드웨어에 맡긴다 |

## 실무에서 기억할 흐름

1. **먼저 측정한다.** Nsight Compute의 Memory Workload Analysis 등을 이용해 global-memory 효율, sector 요청, DRAM throughput, stall을 확인한다.
2. **접근 패턴을 본다.** 인접 thread가 연속된 주소를 읽는지, stride나 random access가 있는지 확인한다.
3. **데이터 재사용을 늘린다.** 같은 데이터를 반복해서 읽는다면 shared-memory tiling을 검토한다.
4. **on-chip 메모리도 점검한다.** Shared memory를 사용하더라도 bank conflict가 있으면 병목이 될 수 있다.
5. **복사와 계산을 겹친다.** 비동기 prefetch, double buffering, TMA를 활용해 메모리 대기 시간을 숨길 수 있는지 확인한다.
6. **최적화 결과를 다시 측정한다.** 각 기법이 모든 커널에서 이득을 주는 것은 아니므로 실제 프로파일링 결과로 검증한다.

## 한 문장으로 정리

**GPU 메모리 최적화는 데이터를 더 적게 낭비하며 가져오고(coalescing/vectorization), 가져온 데이터는 재사용하고(tiling/cache), 데이터 이동 중에도 계산을 계속하게 만드는 것(async prefetch/TMA)이다.**
