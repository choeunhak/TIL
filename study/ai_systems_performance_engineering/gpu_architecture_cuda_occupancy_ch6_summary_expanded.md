# Chapter 6. GPU Architecture, CUDA Programming, and Maximizing Occupancy

> 출처: Chris Fregly, *AI Systems Performance Engineering*

---

## 전체 흐름

GPU에 들어온 데이터를 GPU 내부에서 어떻게 효율적으로 계산하는가

```text
Block size
   ↓
몇 개의 warp가 만들어지는가?
   ↓
Register / Shared Memory를 얼마나 쓰는가?
   ↓
SM에 warp를 몇 개 resident시킬 수 있는가?
   ↓
Occupancy / Latency Hiding
   ↓
실제 Throughput
```

---

# 0. 이 장의 핵심 흐름

GPU 최적화는 단순히 thread를 많이 만드는 문제가 아니다.

```text
충분한 parallelism
+ 적절한 block size
+ register/shared memory 사용량 조절
+ latency hiding
+ memory hierarchy에서 data reuse
+ memory-bound / compute-bound 판별
= 높은 실제 throughput
```

여기서 가장 중요한 사고방식은 **GPU의 목표가 개별 thread 하나를 최대한 빨리 끝내는 것이 아니라, GPU 전체가 계속 일을 하도록 만드는 것**이라는 점이다.

---

# 1. CPU와 GPU의 설계 목표 차이

CPU는 비교적 적은 수의 강력한 core로 개별 작업의 latency를 낮추는 데 강하다.

```text
CPU
→ 적은 수의 강력한 core
→ branch prediction, 큰 cache, out-of-order execution
→ 한 thread의 일을 최대한 빨리 끝냄
```

GPU는 방향이 다르다.

```text
GPU
→ 많은 execution resource
→ 매우 많은 thread를 준비
→ 전체 처리량(throughput)을 높임
```

GPU workload에서는 HBM 같은 memory에서 데이터를 기다리는 상황이 자주 생긴다.

```text
Warp A : HBM 요청 ───────────── 기다림 ─ 계산
Warp B :           계산 계산
Warp C :                    계산 계산
Warp D :                             계산
```

Warp A의 memory latency 자체가 사라진 것은 아니다. A가 기다리는 동안 B/C/D를 실행해서 **SM이 노는 시간을 줄인 것**이다.

이것이 **latency hiding**이다.

CPU의 async I/O와 철학적으로 비슷하게 생각할 수 있다.

```text
CPU async
Task A가 I/O 기다림 → Task B 수행

GPU
Warp A가 memory 기다림 → Warp B 수행
```

차이는 GPU에서는 이런 전환이 SM의 warp scheduler에 의해 하드웨어 수준에서 매우 빠르게 이루어진다는 점이다.

---

# 2. Streaming Multiprocessor (SM)

GPU는 여러 개의 **SM(Streaming Multiprocessor)** 으로 구성된다.

```text
GPU
├─ SM 0
├─ SM 1
├─ SM 2
├─ ...
└─ SM N
```

SM을 쉽게 표현하면 **warp들이 올라와 실제로 일하는 작업장**이다.

SM 안에는 대략 다음 자원이 있다.

```text
Warp Scheduler
FP / INT execution units
Tensor Cores
Load / Store units
Special Function Units
Registers
Shared Memory / L1
TMEM (Blackwell)
```

중요한 구분은 다음과 같다.

```text
GPU 전체
 └─ 여러 SM
      └─ 여러 resident warp
           └─ 각 warp = 32 threads
```

### Resident란?

`resident warp`는 **지금 이 순간 계산 중인 warp**라는 뜻이 아니다.

SM의 register/shared-memory 등의 자원을 이미 배정받고, 그 SM에 올라와 있어 scheduler가 필요할 때 실행할 수 있는 warp를 뜻한다.

```text
SM 안

Warp A → 현재 instruction 실행 중
Warp B → READY, 차례 대기
Warp C → HBM 응답 대기
Warp D → READY, 차례 대기
```

위 네 개는 모두 resident일 수 있다.

즉 직관적으로는 **"미리 SM에 올려놓은 실행 후보들"**이라고 보면 된다.

---

# 3. SIMT: Single Instruction, Multiple Threads

NVIDIA GPU의 핵심 scheduling 단위는 **warp**다.

```text
1 Warp = 32 Threads
```

예를 들어 다음 연산이 있다고 하자.

```cpp
input[idx] *= 2.0f;
```

하나의 warp에서는 대략 다음처럼 동작한다.

```text
Thread 0  → input[0]  * 2
Thread 1  → input[1]  * 2
Thread 2  → input[2]  * 2
...
Thread 31 → input[31] * 2
```

즉 **명령은 같고, 각 thread가 다루는 데이터가 다르다.**

```text
same instruction
      ↓
T0 T1 T2 ... T31
↓  ↓  ↓       ↓
서로 다른 데이터
```

이 실행 모델이 SIMT다.

> 프로그래머는 개별 thread 단위로 코드를 작성하지만, hardware scheduling 관점에서는 32개 thread를 묶은 warp가 매우 중요하다.

---

# 4. Warp Divergence

하나의 warp는 같은 instruction 흐름으로 움직이는 것이 가장 효율적이다.

다음 코드가 있다고 하자.

```cpp
if (condition) {
    A();
} else {
    B();
}
```

한 warp의 thread가 이렇게 갈리면:

```text
Thread 0~15  → A
Thread 16~31 → B
```

32개가 각각 완전히 독립적으로 A와 B를 동시에 수행하는 식으로 처리되는 것이 아니다. 서로 다른 branch 경로를 처리하면서 해당 경로에 참여하지 않는 lane은 비활성화될 수 있다.

개념적으로:

```text
A 경로 실행
T0~15  : ON
T16~31 : OFF

B 경로 실행
T0~15  : OFF
T16~31 : ON
```

따라서 한 warp 내부의 branch가 심하게 갈라지면 실행 효율이 낮아질 수 있다.

중요한 구분:

```text
같은 Warp 내부
절반 A / 절반 B
→ divergence 문제 가능

Warp 0 전체 = A
Warp 1 전체 = B
→ 같은 의미의 intra-warp divergence는 아님
```

---

# 5. Thread → Warp → Block → Grid

CUDA의 논리적 실행 계층은 다음과 같다.

```text
Grid
 ├─ Block 0
 │   ├─ Warp 0 → Thread 0~31
 │   ├─ Warp 1 → Thread 32~63
 │   └─ ...
 ├─ Block 1
 └─ ...
```

### Thread

가장 작은 프로그래밍 단위다.

각 thread는 자기 자신의:

```text
threadIdx
register 값
local state
```

를 가진다.

### Warp

32개 thread를 묶은 핵심 SIMT scheduling 단위다.

### Thread Block

여러 thread를 하나의 그룹으로 묶은 단위다.

같은 block의 thread들은:

- shared memory를 공유할 수 있다.
- `__syncthreads()` 같은 barrier를 이용해 동기화할 수 있다.
- block 전체가 하나의 SM에 배치된다.

### Grid

하나의 kernel launch로 만들어진 모든 block의 집합이다.

예를 들어:

```cpp
myKernel<<<1000, 256>>>(input, N);
```

이면:

```text
Grid
= 1000 Blocks

각 Block
= 256 Threads
= 256 / 32
= 8 Warps
```

전체적으로는 8,000 warp가 만들어지지만, 이 warp들이 한꺼번에 한 SM에 들어가는 것은 아니다. 여러 SM이 block을 받아가며 처리한다.

---

# 6. 왜 block size는 보통 32의 배수인가?

warp가 32 threads이기 때문이다.

```text
256 threads/block
= 8 full warps
```

반면 33 threads라면:

```text
Warp 0 → 32 threads 사용
Warp 1 → 1 thread 사용, 나머지 lane은 활용되지 않음
```

따라서 일반적으로 128, 256, 512 등 32의 배수를 많이 사용한다.

다만 **32의 배수 = 항상 최적**은 아니다.

예를 들어 block을 크게 만들면 warp는 많아지지만, block당 register/shared memory 소비도 커질 수 있어 동시에 resident할 수 있는 block 수가 줄어들 수 있다.

그래서 흔히 256 threads/block을 시작점으로 잡고 실제 profiler/benchmark로 조정한다.

---

# 7. Blackwell의 주요 thread/block limit

책에서 다루는 Blackwell 예시는 다음과 같은 한계를 기준으로 occupancy를 설명한다.

```text
Warp size                     = 32 threads
Max threads / block           = 1,024
Max warps / block             = 32
Max resident warps / SM       = 64
Max resident threads / SM     = 2,048
Max active blocks / SM        = 32
```

예를 들어 thread 수만 생각하면:

```text
Block = 1,024 threads

2,048 / 1,024
= 최대 2 blocks / SM
```

반대로:

```text
Block = 256 threads

2,048 / 256
= 최대 8 blocks / SM
```

하지만 이것은 **thread 수만 본 이론값**이다.

실제로는:

```text
Register 사용량
Shared Memory 사용량
Block 수 제한
Warp 수 제한
```

중 하나가 먼저 한계에 걸려 resident block 수가 더 적어질 수 있다.

---

# 8. CUDA Kernel 기본 구조

가장 기본적인 CUDA kernel을 보자.

```cpp
__global__ void myKernel(float* input, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < N) {
        input[idx] *= 2.0f;
    }
}
```

CUDA에서는 **GPU에서 실행할 함수**를 kernel이라고 부른다.

```cpp
__global__
```

은 **CPU(host)에서 호출하고 GPU(device)에서 실행하는 kernel 함수**라는 뜻이다.

CPU 쪽에서는 일반 함수처럼 `myKernel()`만 호출하지 않고 다음처럼 실행한다.

```cpp
myKernel<<<blocksPerGrid, threadsPerBlock>>>(input, N);
```

여기서 `<<< >>>` 안은 **kernel을 어떤 크기의 병렬 작업으로 실행할지 정하는 launch configuration**이다.

```text
<<< Block 개수, Block당 Thread 개수 >>>
```

즉:

```text
threadsPerBlock
= Block 하나에 thread를 몇 개 만들지

blocksPerGrid
= Grid 전체에 Block을 몇 개 만들지
```

예를 들어:

```cpp
myKernel<<<1000, 256>>>(input, N);
```

이면 논리적으로 다음과 같은 작업을 만든다.

```text
Grid 1개
 ├─ Block 0  → Thread 0 ~ 255
 ├─ Block 1  → Thread 0 ~ 255
 ├─ Block 2  → Thread 0 ~ 255
 ...
 └─ Block 999 → Thread 0 ~ 255
```

따라서 총 thread 수는:

```text
1000 blocks
× 256 threads/block
= 256,000 logical threads
```

이다.

여기서 **256,000개의 thread가 물리적으로 전부 동시에 실행된다는 뜻은 아니다.**

CUDA가 만든 것은 256,000개의 **논리적 작업**이고, 실제 GPU에서는:

```text
Grid
 ↓
Block들이 여러 SM에 배치
 ↓
Block 안의 thread들이 32개씩 Warp로 묶임
 ↓
Warp들이 SM에 resident
 ↓
Warp Scheduler가 실행 가능한 Warp를 선택
```

하는 식으로 조금씩 처리된다.

즉 앞에서 배운 구조와 연결하면:

```text
myKernel<<<1000, 256>>>

        ↓

Grid
= Block 1000개

        ↓

Block 하나
= 256 Threads
= 8 Warps

        ↓

Block들이 여러 SM에 배치

        ↓

Warp들이 resident

        ↓

Warp Scheduler가 실행
```

이다.

그런데 여기서 한 가지 의문이 생긴다.

> 모든 thread가 똑같은 `myKernel()` 코드를 실행한다면 어떻게 서로 다른 데이터를 처리할까?

이를 위해 CUDA는 각 thread에게 자신의 위치를 알려주는 값들을 제공한다.

```text
blockIdx   → 현재 Block의 번호
blockDim   → Block의 크기
threadIdx  → 현재 Block 안에서 Thread의 번호
```

각 thread는 같은 코드를 실행하더라도 이 값들이 다르기 때문에 서로 다른 배열 원소를 담당할 수 있다.

이것이 바로 다음의 **Global Thread Index** 계산으로 연결된다.

---

# 9. Global Thread Index

1차원 배열을 처리할 때 가장 자주 보는 코드다.

```cpp
int idx = blockIdx.x * blockDim.x + threadIdx.x;
```

이 코드는 쉽게 말하면:

> **현재 thread가 전체 Grid에서 몇 번째 thread인지 계산하는 코드**

다.

각 항목의 뜻은 다음과 같다.

```text
blockIdx.x
= 지금 몇 번째 Block인가?

blockDim.x
= Block 하나에 Thread가 몇 개인가?

threadIdx.x
= 이 Block 안에서 나는 몇 번째 Thread인가?
```

예를 들어 kernel을 이렇게 실행했다고 하자.

```cpp
myKernel<<<4, 256>>>(input, N);
```

그러면:

```text
Block 개수 = 4
Block당 Thread = 256
```

이므로 모든 thread에서:

```text
blockDim.x = 256
```

이다.

## Block 0

Block 0의 첫 번째 thread는:

```text
blockIdx.x  = 0
blockDim.x  = 256
threadIdx.x = 0
```

이므로:

```text
idx = 0 × 256 + 0
    = 0
```

따라서 이 thread는:

```cpp
input[0]
```

을 담당한다.

Block 0의 다음 thread들은:

```text
Thread 0   → 0 × 256 + 0   = idx 0
Thread 1   → 0 × 256 + 1   = idx 1
Thread 2   → 0 × 256 + 2   = idx 2
...
Thread 255 → 0 × 256 + 255 = idx 255
```

즉:

```text
Block 0
→ input[0] ~ input[255]
```

를 담당한다.

## Block 1

중요한 점은 **새로운 Block이 시작되면 `threadIdx.x`는 다시 0부터 시작한다는 것**이다.

```text
Block 1
 ├─ Thread 0
 ├─ Thread 1
 ...
 └─ Thread 255
```

따라서 `threadIdx.x`만 사용하면:

```text
Block 0의 Thread 0 → 0
Block 1의 Thread 0 → 0
```

처럼 서로 다른 Block의 thread가 같은 번호를 갖게 된다.

그래서 앞에:

```cpp
blockIdx.x * blockDim.x
```

를 붙여 **앞쪽 Block들이 이미 담당한 thread 수만큼 건너뛴다.**

Block 1의 Thread 0은:

```text
blockIdx.x  = 1
blockDim.x  = 256
threadIdx.x = 0

idx = 1 × 256 + 0
    = 256
```

따라서:

```cpp
input[256]
```

을 담당한다.

계속 계산하면:

```text
Thread 0   → 1 × 256 + 0   = idx 256
Thread 1   → 1 × 256 + 1   = idx 257
...
Thread 255 → 1 × 256 + 255 = idx 511
```

즉:

```text
Block 1
→ input[256] ~ input[511]
```

을 담당한다.

전체를 이어 보면:

```text
Block 0 → input[0]   ~ input[255]
Block 1 → input[256] ~ input[511]
Block 2 → input[512] ~ input[767]
Block 3 → input[768] ~ input[1023]
```

이 된다.

따라서:

```cpp
int idx = blockIdx.x * blockDim.x + threadIdx.x;
```

는 사실상:

```text
앞에 있는 Block들이 가지고 있는 Thread 수
+
현재 Block 안에서 나의 Thread 번호
```

를 계산하는 식이다.

이렇게 만든 `idx`를 사용해서:

```cpp
input[idx] *= 2.0f;
```

를 실행하면 각 thread가 서로 다른 배열 원소를 처리한다.

예를 들어 `N = 1000`이라면 개념적으로:

```text
Global Thread 0   → input[0]   × 2
Global Thread 1   → input[1]   × 2
Global Thread 2   → input[2]   × 2
...
Global Thread 999 → input[999] × 2
```

처럼 병렬 작업이 나뉜다.

즉 8번과 9번을 연결하면:

```text
8번: <<<blocks, threads>>>

"GPU에서 병렬 작업을 몇 개 만들 것인가?"

        ↓

Grid → Blocks → Threads


9번: blockIdx * blockDim + threadIdx

"각 Thread가 어떤 데이터를 담당할 것인가?"

        ↓

input[idx]
```

라고 이해하면 된다.

참고로 `.x`가 붙는 이유는 CUDA의 Block과 Grid가 1차원뿐 아니라 2차원, 3차원으로도 구성될 수 있기 때문이다.

```text
threadIdx.x
threadIdx.y
threadIdx.z
```

처럼 좌표를 가질 수 있고, 지금 예제는 **1차원 배열**을 처리하므로 `.x`만 사용한다.

---

# 10. Bounds Check

데이터 개수가 block size의 배수가 아닐 수 있다.

```text
N = 1000
threadsPerBlock = 256
```

3 block이면:

```text
3 × 256 = 768
```

부족하다.

따라서 4 block이 필요하다.

```text
4 × 256 = 1024 threads
```

하지만 실제 데이터는 1000개뿐이므로:

```text
idx 1000~1023
```

은 처리할 데이터가 없다.

그래서:

```cpp
if (idx < N) {
    input[idx] *= 2.0f;
}
```

처럼 검사한다.

이 조건이 없으면 존재하지 않는 배열 범위에 접근해 illegal memory access가 발생할 수 있다.

CUDA는 kernel 실행이 asynchronous한 경우가 많아서 GPU 내부 오류가 launch 줄에서 즉시 CPU exception처럼 보이지 않고, 이후 synchronization/API 호출에서 드러날 수도 있다.

---

# 11. `blocksPerGrid` 계산

보편적으로 다음 식을 쓴다.

```cpp
int blocksPerGrid =
    (N + threadsPerBlock - 1) / threadsPerBlock;
```

이 식은 **정수 나눗셈으로 ceiling(올림)을 만드는 패턴**이다.

예를 들어:

```text
N = 1000
threadsPerBlock = 256
```

이면:

```text
(1000 + 256 - 1) / 256
= 1255 / 256
= 4      // integer division
```

즉 필요한 데이터가 조금이라도 남으면 마지막 block 하나를 더 만든다.

마지막 block에서 남는 thread는 앞의 `if (idx < N)`이 막아준다.

정리:

```text
blocksPerGrid 계산
→ 데이터 전체를 덮을 만큼 thread 생성

bounds check
→ 초과 생성된 thread가 잘못된 memory를 건드리지 않게 함
```

---

# 12. 2D / 3D Kernel

이미지나 행렬은 1D index 하나보다 x/y 좌표를 쓰는 것이 자연스럽다.

```cpp
dim3 threadsPerBlock(16, 16);
```

의미는:

```text
16 × 16
= 256 threads/block
```

이다.

각 thread의 global coordinate는:

```cpp
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;
```

로 계산한다.

1D와 원리는 완전히 같다.

```text
1D
global index = block 시작 위치 + block 안의 내 위치

2D
x = x 방향 block 시작 위치 + block 안의 x

y = y 방향 block 시작 위치 + block 안의 y
```

이미지라면 한 thread가 pixel 하나를 담당하도록 만들 수 있다.

3D volume도 `dim3(x, y, z)`로 같은 원리를 확장한다.

---

# 13. CUDA Forward / Backward Compatibility

CUDA 코드를 compile하면 GPU가 직접 실행할 수 있는 architecture-specific code와 PTX 같은 intermediate representation을 포함할 수 있다.

개념적으로:

```text
CUDA C++
   ↓
 PTX     ← 비교적 중간 표현에 가까움
   ↓ JIT / compile
SASS     ← 실제 GPU instruction
```

배포 binary에 현재 GPU용 code뿐 아니라 PTX도 넣어두면, 미래 GPU에서 driver가 PTX를 해당 GPU용 code로 JIT compile할 수 있다.

```text
현재 GPU용 cubin/SASS
+
PTX fallback
```

`CUDA_FORCE_PTX_JIT=1`은 실제로 PTX JIT path가 동작하는지 확인할 때 사용할 수 있다.

---

# 14. Synchronous Allocation의 비용

전통적인 GPU memory allocation:

```cpp
cudaMalloc(...);
cudaFree(...);
```

은 단순한 pointer 연산보다 훨씬 비싼 작업이다.

allocation/free 과정에서는 runtime/driver 수준의 관리가 필요하고, 경우에 따라 synchronization 비용도 생길 수 있다.

그래서 반복 loop에서:

```text
allocate
kernel
free
allocate
kernel
free
...
```

를 계속 수행하면 실제 kernel보다 allocator overhead가 눈에 띌 수 있다.

CPU 애플리케이션에서 매 요청마다 큰 memory를 OS에서 새로 할당하는 것이 비효율적인 것과 비슷하게 생각할 수 있다.

---

# 15. `cudaMallocAsync` / `cudaFreeAsync`

CUDA는 stream-ordered asynchronous allocation을 제공한다.

```cpp
cudaMallocAsync(..., stream);
cudaFreeAsync(..., stream);
```

핵심 아이디어는 **memory pool 재사용**이다.

```text
cudaMallocAsync
      ↓
 CUDA Memory Pool
      ↓
 이미 확보된 memory 재사용
      ↓
cudaFreeAsync
```

즉 매번 system 수준에서 새 memory를 받고 반환하기보다, runtime이 이미 확보한 GPU memory를 pool에 두고 재사용한다.

장점:

```text
allocation overhead 감소
불필요한 synchronization 감소
stream과 자연스럽게 순서 관리
```

PyTorch의 caching allocator 역시 큰 방향은 비슷하다.

---

# 16. GPU Memory Hierarchy

GPU memory는 전부 같은 장소, 같은 속도가 아니다.

큰 그림:

```text
빠름 / 작음 / 가까움
↑
Registers
Shared Memory / L1
TMEM
Constant Cache
L2
Global Memory / HBM
Host Memory
↓
느림 / 큼 / 멂
```

> `local memory`는 이름 때문에 가까워 보이지만 주의해야 한다. CUDA에서 thread-local address space를 뜻하며, register spill 등에 사용될 경우 물리적으로는 device memory 쪽에 놓이고 cache를 거칠 수 있다.

최적화의 가장 중요한 원칙 중 하나:

> **HBM에서 가져온 데이터를 가능하면 register/shared/cache에서 많이 재사용하자.**

예:

```text
나쁜 경우
HBM → A 읽음
HBM → A 또 읽음
HBM → A 또 읽음

좋은 경우
HBM → A 한 번 읽음
        ↓
     Shared/Register
        ↓
     여러 번 reuse
```

---

# 17. Registers와 Register Spill

Register는 thread가 사용하는 local variable을 저장하는 매우 빠른 on-chip storage다.

개념적으로:

```cpp
float a;
float b;
float c;
```

같은 값을 가능한 한 register에 두면 연산할 때 매우 빠르게 사용할 수 있다.

하지만 register는 무한하지 않다.

### Register pressure

하나의 thread가 동시에 너무 많은 값을 유지하려 하면 많은 register가 필요하다.

```text
Thread 하나
→ register 20개 필요

보다

Thread 하나
→ register 150개 필요

가 SM의 register pool을 훨씬 많이 소비
```

### Spill이란?

register에 넣어두고 싶은 값을 register 공간/할당 제약 때문에 memory 쪽으로 밀어내는 것이다.

```text
Registers
[a][b][c][d]  ← 여기에 두고 싶음

공간/할당 부족
      ↓
 e, f 일부가 밖으로 밀림
      ↓
Register Spill
      ↓
Local Memory address space
      ↓
cache miss 시 device memory/HBM 접근 가능
```

`spill이 비싸다`는 말은 돈이 비싸다는 뜻이 아니라 **성능 비용이 크다**는 뜻이다.

원래 register에 있으면:

```text
값 읽음
→ 바로 계산
```

spill되면:

```text
memory load
→ cache/HBM에서 데이터 도착 대기 가능
→ 계산
→ 필요하면 다시 store
```

처럼 load/store instruction과 memory traffic이 추가된다.

### 그렇다면 register를 무조건 많이 주면 좋은가?

그것도 아니다.

SM의 전체 register 수는 제한되어 있기 때문에:

```text
registers/thread ↑
      ↓
한 thread/block이 차지하는 register ↑
      ↓
SM에 동시에 올릴 수 있는 thread/warp ↓
      ↓
occupancy ↓ 가능
```

따라서 trade-off가 있다.

```text
register 너무 적음
→ spill 가능

register 너무 많음
→ resident warp 감소 가능

목표
→ 실제 throughput 최대화
```

---

# 18. Shared Memory / L1

Shared Memory는 **같은 block의 thread들이 함께 사용할 수 있는 빠른 on-chip memory**다.

```text
Thread Block
 ├─ Thread 0 ─┐
 ├─ Thread 1 ─┤
 ├─ Thread 2 ─┼→ Shared Memory
 └─ Thread N ─┘
```

HBM과 차이:

```text
HBM
→ GPU의 큰 device memory
→ 용량 큼
→ 모든 SM에서 접근 가능
→ latency 큼

Shared Memory
→ SM 내부 on-chip
→ 매우 작음
→ 같은 block의 thread끼리 공유
→ 훨씬 빠름
```

### 왜 Shared Memory를 쓰는가?

같은 데이터를 여러 thread가 반복해서 사용할 때 HBM에서 매번 읽지 않기 위해서다.

```text
HBM
 ↓ 한 번 load
Shared Memory
 ↓ ↓ ↓ ↓
T0 T1 T2 T3가 여러 번 reuse
```

행렬곱에서 tile 단위로 데이터를 shared memory에 올려 재사용하는 것이 대표적이다.

### Shared Memory도 너무 많이 쓰면 문제가 된다

예를 들어 한 SM에서 사용할 수 있는 shared-memory budget을 100이라고 가정하자.

```text
Block A가 70 사용
남은 공간 30

Block B도 70 필요
→ 동시에 못 올라옴
```

결과:

```text
shared memory / block ↑
        ↓
resident blocks / SM ↓
        ↓
resident warps ↓
        ↓
occupancy ↓
```

따라서 shared memory도 **많이 쓰면 무조건 좋은 것**이 아니다.

---

# 19. TMEM

Blackwell에서는 Tensor Core workload를 위한 **Tensor Memory(TMEM)** 개념이 중요해진다.

일반적인 CUDA pointer로 마음대로 읽고 쓰는 보통 memory와는 성격이 다르며, Tensor Core operation의 accumulator와 data movement를 효율적으로 지원한다.

큰 그림은 다음 정도로 이해하면 충분하다.

```text
Global Memory / HBM
        ↓
       TMA
        ↓
Shared Memory
        ↓
Tensor Core
    ↕
   TMEM
```

여기서 목표는 **Tensor Core가 데이터를 기다리지 않고 matrix compute를 계속할 수 있도록 data movement를 효율화하는 것**이다.

지금 단계에서는 TMEM 세부 instruction보다 다음 연결이 더 중요하다.

```text
데이터 이동 효율화
→ Tensor Core waiting 감소
→ 실제 compute utilization 증가
```

---

# 20. Constant Memory Cache

Constant memory는 작고 read-only이며, 많은 thread가 같은 값을 읽는 상황에서 유리하다.

예:

```text
lookup table
RoPE 관련 상수
ALiBi slope
quantization scale
```

하나의 warp에서 32개 thread가 같은 address를 읽는다면 broadcast 형태로 효율적으로 전달할 수 있다.

```text
32 threads
   ↓ 모두 같은 address 요청
constant cache
   ↓
한 값을 warp 전체에 전달
```

반대로 thread마다 서로 다른 constant address를 읽으면 장점이 줄고 access가 serialize될 수 있다.

---

# 21. L2 Cache

L2 cache는 여러 SM이 공유한다.

```text
SM 0 ─┐
SM 1 ─┤
SM 2 ─┼→ L2 → HBM
SM 3 ─┘
```

Shared Memory가 **block/SM에 가까운 명시적 작업 공간**이라면, L2는 GPU 전체 차원의 cache 역할을 한다.

예를 들어 어떤 block이 HBM에서 읽은 데이터가 L2에 남아 있고 다른 block이 다시 필요로 한다면:

```text
HBM까지 다시 접근
```

하지 않고 L2 hit로 처리될 수 있다.

또 global memory access가 aligned/coalesced하면 cache line과 DRAM bandwidth를 더 효율적으로 사용할 수 있다.

coalescing은 Chapter 7에서 더 깊게 보는 개념이지만, 지금은:

> **warp의 thread들이 memory를 제멋대로 읽는 것보다 연속된 주소를 잘 묶어 읽는 것이 효율적이다.**

정도로 이해하면 된다.

---

# 22. Global Memory / HBM

HBM은 GPU의 큰 device memory다.

```text
GPU
├─ SM
├─ SM
├─ SM
│
└─ L2
    ↓
   HBM
```

특징:

```text
용량 큼
bandwidth 매우 큼
하지만 register/shared memory보다 latency 큼
```

여기서 중요한 점:

> **bandwidth가 높다고 latency가 낮은 것은 아니다.**

비유하면 HBM은 차선이 엄청 많은 고속도로다.

```text
차선 수 많음
→ 한꺼번에 많은 데이터 이동 가능
→ bandwidth 높음

거리는 멂
→ 한 요청의 응답까지는 시간이 필요
→ latency 존재
```

그래서 GPU는 HBM latency를 없애기보다:

```text
Warp A → HBM 기다림
Warp B → 실행
Warp C → 실행
```

처럼 다른 warp를 실행해 latency를 숨긴다.

이것이 memory hierarchy와 occupancy가 연결되는 지점이다.

---

# 23. Unified Memory

CUDA Managed/Unified Memory는 CPU와 GPU에서 사용할 memory를 하나의 abstraction으로 다루기 편하게 해준다.

하지만 편리함이 **물리적 데이터 이동이 없어졌다는 뜻은 아니다.**

예:

```text
page가 CPU 쪽에 있음
      ↓
GPU가 갑자기 접근
      ↓
page migration 필요
      ↓
unexpected stall 가능
```

그래서 다음처럼 미리 알려줄 수 있다.

```cpp
cudaMemPrefetchAsync(...);
```

의미는 대략:

> "곧 GPU가 이 데이터를 사용할 예정이니 미리 GPU 쪽에 가져다 놓자."

Chapter 5의 prefetch와 같은 철학이다.

```text
필요해진 뒤 가져옴
→ 기다림 발생

필요하기 전에 미리 가져옴
→ 기다림을 다른 작업과 overlap
```

---

# 24. Occupancy란?

Occupancy는 한 SM이 가질 수 있는 최대 resident warp 수 대비 현재 resident한 warp 수의 비율로 이해하면 된다.

```text
Occupancy
≈ Resident Warps / Maximum Resident Warps
```

예를 들어 최대 64 warp를 resident시킬 수 있는 SM에서:

```text
32 resident warps
→ 50%

64 resident warps
→ 100%
```

### 여기서 가장 자주 하는 오해

`resident warp` 또는 occupancy 계산의 `active warp`를 **그 순간 모두 계산 중인 warp**로 이해하면 안 된다.

```text
Resident Warp A → 실행 중
Resident Warp B → READY
Resident Warp C → memory wait
Resident Warp D → dependency wait
```

모두 SM에 올라와 있을 수 있다.

### Occupancy가 왜 중요한가?

Latency hiding 때문이다.

resident warp가 2개뿐인데 둘 다 HBM을 기다린다면:

```text
Warp A → wait
Warp B → wait
SM     → 실행할 warp 없음
```

SM이 놀 수 있다.

반면 resident warp가 충분히 많다면:

```text
A → wait
B → wait
C → READY
D → READY
E → READY
```

scheduler가 C/D/E를 실행할 수 있다.

즉:

```text
resident warp 충분
      ↓
ready warp가 존재할 확률 증가
      ↓
latency hiding 쉬움
      ↓
execution unit idle 감소
```

---

# 25. Occupancy를 제한하는 자원

thread를 많이 launch한다고 occupancy가 자동으로 높아지는 것은 아니다.

한 SM에는 한계가 있다.

```text
Threads / SM
Warps / SM
Blocks / SM
Registers / SM
Shared Memory / SM
```

이 중 **가장 먼저 한계에 걸리는 자원**이 실제 resident block/warp 수를 제한한다.

### Register 예시

가상의 SM에 register가 65,536개 있다고 하자.

Block이 256 threads이고 thread당 register를 32개 쓴다면:

```text
256 × 32
= 8,192 registers / block
```

register 기준으로는 여러 block을 올릴 여지가 있다.

thread당 register를 128개 쓰면:

```text
256 × 128
= 32,768 registers / block
```

두 block만으로 65,536개가 된다.

즉:

```text
registers/thread ↑
       ↓
resident blocks ↓
       ↓
resident warps ↓
       ↓
occupancy ↓
```

### Shared Memory 예시

```text
SM shared memory budget = 100

Block A = 60
Block B = 60
```

A 하나를 올리면 40밖에 남지 않아 B를 같이 resident시키지 못한다.

```text
shared memory/block ↑
       ↓
resident blocks ↓
       ↓
occupancy ↓
```

---

# 26. 높은 Occupancy가 항상 최고 성능은 아니다

```text
Occupancy 100%
≠ 항상 최고 성능
```

Occupancy는 **목표가 아니라 latency hiding을 위한 수단**이다.

예를 들어 원래 kernel이:

```text
register/thread = 80
occupancy = 50%
spill 거의 없음
```

이라고 하자.

occupancy를 100%로 만들려고 compiler에게 register를 32개만 쓰게 강제하면:

```text
register 부족
   ↓
spill 증가
   ↓
local/global memory load/store 증가
   ↓
memory latency/traffic 증가
   ↓
오히려 kernel 느려짐
```

가능하다.

즉 두 방향 사이의 균형이 필요하다.

```text
Register 넉넉히 사용
→ 개별 thread 계산 효율 ↑
→ 하지만 resident warp ↓ 가능

Register 과도하게 제한
→ resident warp ↑ 가능
→ 하지만 spill ↑ 가능
```

최종 목표:

```text
Occupancy MAX ❌

실제 Kernel Throughput MAX ✅
```

---

# 27. Launch Bounds

CUDA의 `__launch_bounds__`는 compiler에게 kernel의 예상 launch 조건을 알려주는 힌트다.

예를 들어 개념적으로:

```cpp
__global__ __launch_bounds__(256, 2)
void myKernel(...) {
    ...
}
```

은 compiler가 다음과 같은 정보를 고려하게 한다.

```text
Block당 최대 thread 수는 256 정도
SM에 최소 2 block이 resident할 수 있게 고려
```

compiler는 이를 바탕으로 register allocation 등을 조정할 수 있다.

하지만 여기서도 무리하게 occupancy를 강제하면 register 제한 → spill로 이어질 수 있다.

따라서:

```text
launch_bounds 설정
      ↓
compile
      ↓
Nsight / benchmark
      ↓
실제 throughput 확인
```

이 필요하다.

---

# 28. Functional Correctness: Compute Sanitizer

성능 최적화보다 먼저 코드가 정확해야 한다.

CUDA는 asynchronous execution이 많아서 오류가 발생한 위치와 CPU에서 오류를 확인하는 시점이 다를 수 있다.

Compute Sanitizer로 대표적으로 다음을 찾을 수 있다.

```text
invalid memory access
race condition
uninitialized memory
synchronization problem
```

특히 bounds check 실수, shared-memory synchronization 오류 등을 잡을 때 중요하다.

순서는:

```text
Correctness
   ↓
Profiling
   ↓
Optimization
```

이 안전하다.

잘못된 결과를 빠르게 만드는 것은 최적화가 아니다.

---

# 29. Roofline Model

Roofline은 **내 kernel이 왜 느린지**를 크게 두 방향으로 나눠 생각하게 해준다.

```text
Memory-bound
vs
Compute-bound
```

핵심 지표는 Arithmetic Intensity다.

```text
Arithmetic Intensity
= 수행한 FLOPs / memory에서 이동한 Bytes
```

### Arithmetic Intensity가 낮은 예

```text
4 byte 값을 읽음
→ +1 한 번
→ 다시 저장
```

데이터 이동에 비해 계산이 매우 적다.

```text
memory 많이 사용
compute 적음
→ memory-bound 가능성 ↑
```

### Arithmetic Intensity가 높은 예

```text
데이터를 한 번 읽음
→ 그 데이터를 이용해 수백~수천 번 계산
```

```text
memory 이동 대비 compute 많음
→ compute-bound 방향
```

행렬곱은 data reuse를 잘하면 arithmetic intensity가 높아질 수 있는 대표 workload다.

---

# 30. Roofline을 직관적으로 보기

```text
Performance
  ^
  |                    ───────────── Compute Ceiling
  |                  /
  |                /
  |              /
  |            /
  |          /
  |_________/____________________________> Arithmetic Intensity
       Memory-bound          Compute-bound
```

왼쪽에서는 memory bandwidth가 성능 상한을 만든다.

```text
연산기는 더 계산할 수 있음
하지만 데이터가 충분히 빨리 안 옴
```

오른쪽에서는 compute capability가 상한이다.

```text
데이터는 충분히 있음
하지만 CUDA/Tensor Core가 이미 바쁨
```

따라서 병목이 어디인지에 따라 최적화 방법이 완전히 달라진다.

---

# 31. Memory-bound Kernel 최적화 방향

Memory-bound인데 CUDA Core instruction 몇 개를 줄이는 것만으로는 큰 효과가 없을 수 있다.

중요한 방향:

```text
Memory traffic 감소
Data reuse 증가
Coalesced access
Register / Shared Memory 활용
Cache locality 개선
더 작은 precision
Prefetch / overlap
```

예를 들어:

```text
Before
HBM → A
HBM → A
HBM → A
HBM → A
```

보다:

```text
After
HBM → A 한 번
      ↓
Shared/Register
      ↓
4번 reuse
```

가 훨씬 효율적일 수 있다.

FP32를 FP16으로 줄일 수 있는 workload라면 같은 byte bandwidth로 더 많은 element를 옮길 수 있다는 점에서도 유리하다.

---

# 32. Compute-bound Kernel 최적화 방향

Compute-bound에서는 memory bandwidth보다 연산 자원이 병목이다.

이때는 다음을 본다.

```text
Tensor Core 활용
BF16 / FP16 / FP8 등 lower precision
불필요한 instruction 감소
Instruction-Level Parallelism(ILP)
Kernel fusion
더 효율적인 algorithm
```

예를 들어 Tensor Core로 처리할 수 있는 matrix operation을 일반 CUDA Core 방식으로 수행한다면 compute throughput을 제대로 활용하지 못할 수 있다.

반대로 이미 Tensor Core가 거의 최대 utilization이라면 memory 최적화를 더 해도 성능 향상이 작을 수 있다.

따라서 "GPU가 느리다"가 아니라:

```text
무엇을 기다리고 있는가?
```

를 profiler로 확인하는 것이 중요하다.
---

# Key Takeaways

1. GPU는 개별 thread의 latency보다 전체 throughput을 높이도록 설계됐다.
2. 실제 GPU 실행을 이해할 때는 **SM과 warp**가 핵심이다.
3. `1 warp = 32 threads`이며, block size는 보통 32의 배수로 시작한다.
4. `blockIdx`, `blockDim`, `threadIdx`를 이용해 각 thread가 담당할 global index를 계산한다.
5. `if (idx < N)`은 마지막 block의 extra thread가 범위를 벗어나지 않게 한다.
6. **Resident warp**는 SM 자원을 할당받고 실행 가능 상태로 올라와 있는 warp이지, 전부 동시에 계산 중이라는 뜻이 아니다.
7. HBM은 bandwidth는 매우 높지만 on-chip memory보다 latency가 크므로 data reuse와 latency hiding이 중요하다.
8. Shared Memory는 같은 block의 thread가 공유하는 빠른 on-chip 공간이고, HBM은 GPU의 큰 device memory다.
9. Register가 부족하면 값이 local-memory address space로 **spill**될 수 있고 load/store 비용이 늘어난다.
10. Register를 너무 많이 써도 resident warp 수가 줄어 occupancy가 낮아질 수 있다.
11. Shared Memory 사용량도 resident block 수를 제한한다.
12. Occupancy는 latency hiding에 도움을 주지만 **100% 자체가 목표가 아니다.**
13. 목표는 항상 실제 kernel throughput이다.
14. Roofline으로 memory-bound / compute-bound를 먼저 구분하고 병목에 맞춰 최적화한다.
15. 최종 판단은 Nsight Compute / Nsight Systems와 실제 benchmark로 한다.

---
