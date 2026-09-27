# Chapter 6. GPU 아키텍처, CUDA 프로그래밍, Occupancy

> 출처: Chris Fregly, *AI Systems Performance Engineering*  
> 범위: Chapter 6 — *GPU Architecture, CUDA Programming, and Maximizing Occupancy*

## 이 장의 범위

이 장은 CUDA kernel이 GPU에서 어떻게 실행되는지, thread·warp·block·grid가 SM에 어떻게 배치되는지, GPU 메모리 계층과 occupancy를 어떻게 해석하는지를 설명한다. 마지막에는 roofline 모델로 kernel이 연산 제한인지 메모리 제한인지 판별한다.

---

## 1. GPU 실행 구조와 SIMT

CPU는 소수의 thread에서 낮은 지연 시간을 줄이는 데 강하고, GPU는 많은 thread를 동시에 실행해 높은 처리량을 내는 데 초점이 있다.

일반적인 CUDA 흐름은 다음과 같다.

```text
CPU(host) 메모리 할당
→ GPU(device) 메모리로 H2D 복사
→ CPU가 kernel launch
→ GPU가 kernel 실행
→ 필요하면 D2H 복사
```

GPU는 여러 개의 SM(Streaming Multiprocessor)으로 구성된다. SM은 많은 warp를 유지하다가, 어떤 warp가 메모리를 기다리면 준비된 다른 warp를 실행해 지연 시간을 숨긴다.

### Warp와 SIMT

- CUDA warp는 32개 thread의 묶음이다.
- 한 warp의 thread는 같은 instruction을 lockstep으로 실행하는 SIMT 모델을 따른다.
- thread별 데이터와 index는 다를 수 있지만, 같은 warp 안에서 제어 흐름이 갈라지면 branch를 순차적으로 실행해야 한다.
- 서로 다른 warp는 서로 다른 branch를 실행해도 직접적인 divergence penalty가 없다.

Blackwell 예시에서 SM은 최대 64 warp, 즉 2,048 thread를 resident 상태로 유지할 수 있다. 여러 warp scheduler가 준비된 warp의 instruction을 발행하며, 독립적인 연산과 메모리 instruction을 함께 발행할 수 있는 경우 처리량이 높아진다. 정확한 pipeline 수와 issue 동작은 아키텍처별로 다르므로 실제 병목은 profiler counter로 확인해야 한다.

### Warp divergence

같은 warp 안에서 일부 thread가 `if` 경로로, 다른 thread가 `else` 경로로 가면 하드웨어는 각 경로를 차례로 실행하고 해당 경로에 속하지 않는 lane을 마스킹한다. 따라서 warp 내부의 분기가 많을수록 유효 실행 시간이 늘어난다.

분기 자체를 무조건 없애기보다, 같은 warp의 thread가 가능한 한 같은 경로를 따르도록 데이터와 작업을 배치하는 것이 중요하다.

---

## 2. thread, block, grid

CUDA의 작업 계층은 다음과 같다.

```text
thread 32개 = warp 1개
여러 warp = thread block(CTA)
여러 block = grid(kernel launch 전체)
```

- **thread**: kernel 코드를 실행하는 가장 작은 논리 단위
- **warp**: 하드웨어가 실제로 함께 스케줄하는 32 thread 단위
- **block / CTA**: shared memory와 block 내부 동기화를 공유하는 thread 묶음
- **grid**: 한 번의 kernel launch로 실행되는 모든 block의 집합

현대 GPU에서 block은 최대 1,024 thread를 가질 수 있다. block들은 독립적으로 실행되고 실행 순서는 보장되지 않는다. 그래서 grid 크기만 키우면 kernel 코드를 바꾸지 않고 더 많은 SM에 작업을 분배할 수 있다.

### block 안의 협업

한 block의 thread는 on-chip shared memory를 공유하고 `__syncthreads()`로 동기화할 수 있다. shared memory는 데이터 재사용에 유용하지만 barrier에는 비용이 있다. 불필요한 동기화는 줄여야 한다.

최신 CUDA는 여러 block이 thread block cluster를 구성하고, cluster 내부에서 DSMEM(distributed shared memory)과 cluster-scoped barrier를 쓰는 기능도 제공한다. 다만 일반적인 kernel의 기본 단위는 여전히 block 내부 shared memory와 동기화다.

---

## 3. block 크기와 grid 크기 선택

### block 크기는 32의 배수부터 시작

warp가 32 thread이므로 `threadsPerBlock`은 보통 32의 배수로 정한다. 예를 들어 256 thread block은 8개의 꽉 찬 warp로 구성된다. 33 thread block은 두 번째 warp의 대부분 lane이 비어도 warp slot 하나를 사용하므로 비효율적이다.

```cpp
int threadsPerBlock = 256;  // 흔한 시작값: 8 warps
int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;
kernel<<<blocksPerGrid, threadsPerBlock>>>(...);
```

`256`은 좋은 시작점일 뿐 정답은 아니다. 128, 256, 512 등을 profiler로 비교해야 한다.

### block 크기를 제한하는 자원

SM에 동시에 resident할 수 있는 block·warp 수는 다음 중 가장 먼저 닿는 제한에 의해 결정된다.

- SM의 최대 resident thread/warp 수
- block당 thread 수
- thread당 register 사용량
- block당 shared memory 사용량
- SM당 active block 수

Blackwell B200의 대표적인 상한은 warp당 32 thread, block당 최대 1,024 thread, SM당 최대 64 resident warp(2,048 thread), SM당 최대 32 active block이다. GPU 세대마다 세부 제한이 달라지므로 target GPU의 tuning guide를 확인해야 한다.

block을 작게 하면 더 많은 block이 SM에 올라갈 수 있지만 scheduling overhead와 작업량 분할 문제가 생길 수 있다. block이 너무 크거나 register/shared memory를 많이 쓰면 동시에 올라갈 block 수가 줄어 occupancy가 낮아질 수 있다.

---

## 4. CUDA kernel의 기본 형태

CUDA C++ kernel은 `__global__`로 선언하고 CPU host code에서 `<<<grid, block>>>` 문법으로 launch한다.

```cpp
__global__ void scale(float* x, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        x[idx] *= 2.0f;
    }
}

int threads = 256;
int blocks = (N + threads - 1) / threads;
scale<<<blocks, threads>>>(d_x, N);
```

### index와 bounds check

`blockIdx`, `blockDim`, `threadIdx`를 조합하면 각 thread가 처리할 고유 index를 구할 수 있다. `N`이 block 크기의 배수가 아니면 마지막 block에 범위를 벗어난 thread가 생기므로 `if (idx < N)` 검사가 필요하다.

CUDA kernel 안의 잘못된 메모리 접근은 thread별 예외로 바로 전달되지 않는다. launch 전체에 fault 상태가 기록되고 이후 동기화 또는 CUDA API 호출에서 `cudaErrorIllegalAddress` 같은 오류가 나타날 수 있다. 개발 중에는 launch 직후 `cudaGetLastError()`와 적절한 동기화를 사용해 오류 위치를 빨리 찾는다.

### 2D/3D 데이터

이미지나 volume처럼 차원이 있는 입력에는 `dim3`로 2D/3D block과 grid를 만들 수 있다.

```cpp
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;
if (x < width && y < height) {
    int idx = y * width + x;
    // input[idx] 처리
}
```

차원은 입력 형태를 자연스럽게 표현하기 위한 것이고, 결국 모든 thread는 같은 물리 GPU 자원 위에서 실행된다.

---

## 5. CUDA 호환성: cubin, SASS, PTX

CUDA binary는 특정 GPU 아키텍처용 기계어(SASS/cubin)와, 이후 GPU에서 JIT 컴파일할 수 있는 PTX를 포함할 수 있다.

- 특정 `sm_`용 SASS만 넣으면 더 새로운 아키텍처에서 그대로 실행되지 않을 수 있다.
- PTX를 함께 넣으면 새 GPU에서 driver가 JIT하여 forward compatibility를 제공할 수 있다.
- 최신 기능의 최적화가 필요하면 세대 전용 target을 추가하되, 다른 GPU용 fallback도 포함한다.

배포 binary에는 여러 target의 cubin과 PTX를 함께 담은 fatbin을 고려한다. `CUDA_FORCE_PTX_JIT=1`으로 PTX JIT을 강제해, PTX가 빠진 binary를 사전에 확인할 수 있다.

---

## 6. 비동기 할당과 CUDA memory pool

전통적인 `cudaMalloc`/`cudaFree`는 동기화와 driver/OS 수준 작업을 동반할 수 있어, 반복적인 작은 할당·해제에서는 비용이 커질 수 있다.

```cpp
cudaStream_t stream;
cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking);

float* d_buf = nullptr;
cudaMallocAsync(&d_buf, bytes, stream);
kernel<<<grid, block, 0, stream>>>(d_buf);
cudaFreeAsync(d_buf, stream);
```

`cudaMallocAsync`/`cudaFreeAsync`는 stream 순서를 따르고 CUDA memory pool에서 버퍼를 재사용한다.

- free는 해당 stream의 앞선 작업이 끝난 뒤 수행된다.
- 다른 stream까지 기다리는 전역 `cudaDeviceSynchronize()`를 피할 수 있다.
- OS/driver allocation 반복과 fragmentation을 줄이고 지연 시간의 변동을 낮춘다.

pool이 너무 많은 메모리를 유지하면 footprint가 커질 수 있다. `cudaMemPoolAttrReleaseThreshold`, `cudaMemPoolTrimTo` 등으로 재사용성과 메모리 반환 사이의 균형을 조정할 수 있다.

PyTorch의 caching allocator도 매 tensor마다 `cudaMalloc`을 호출하지 않고 버퍼를 재사용한다. 관련 설정은 `PYTORCH_ALLOC_CONF`로 조정할 수 있다.

---

## 7. GPU 메모리 계층

GPU 메모리는 용량이 큰 대신 느린 계층에서, 작지만 빠른 on-chip 계층으로 나뉜다.

```text
register
→ shared memory / L1
→ L2
→ global memory(HBM)
→ CPU host memory
```

### Register와 local memory

register는 thread별로 쓰는 가장 빠른 on-chip 저장소다. 그러나 thread가 register를 너무 많이 쓰면 compiler가 넘치는 값을 local memory에 spill할 수 있다. local memory는 이름과 달리 보통 HBM에 backing되므로 지연 시간이 크다.

register 사용량은 occupancy에도 직접 영향을 준다. thread당 register가 많으면 SM에 동시에 resident할 수 있는 warp 수가 줄어든다.

### Shared memory와 L1

shared memory는 block 안의 thread가 명시적으로 공유하는 on-chip SRAM이다. 같은 데이터 tile을 여러 thread가 재사용할 때 global memory 접근을 줄인다.

- block 내부에서만 공유한다.
- 필요하면 barrier로 읽기/쓰기 순서를 맞춘다.
- bank conflict가 생기지 않게 접근 패턴을 설계한다.
- Blackwell에서는 shared memory와 L1이 같은 on-chip 자원을 나누어 사용한다.

### Constant memory

작은 read-only 테이블에는 constant memory가 적합하다. warp의 모든 thread가 같은 주소를 읽으면 broadcast가 가능하다. 반대로 각 thread가 다른 주소를 읽으면 이점이 줄고 접근이 직렬화될 수 있다.

### L2와 HBM global memory

L2는 모든 SM이 공유하는 GPU-wide cache이고, HBM은 device-wide global memory다. HBM은 매우 높은 대역폭을 제공하지만 on-chip 메모리보다 지연 시간이 훨씬 크다.

global load는 warp의 thread들이 연속적이고 정렬된 주소를 읽도록 설계해 coalesced transaction을 만들면 좋다. 보통 128-byte 정렬·연속 접근이 cache line과 DRAM transaction을 효율적으로 사용한다.

### Blackwell의 TMEM과 TMA

Blackwell에는 Tensor Core 연산을 위한 TMEM(Tensor Memory)이 있다. 이는 일반 CUDA C++ pointer로 직접 접근하는 메모리 공간이 아니라, Tensor Core instruction과 TMA(Tensor Memory Accelerator)가 데이터 이동을 조율하는 전용 on-chip 메모리다.

- TMA: global memory와 shared memory 사이의 큰 tile 이동을 비동기로 처리
- TMEM: Tensor Core 연산의 operand/accumulator를 위한 전용 저장소
- 목적: SM이 주소 계산과 데이터 이동에 쓰는 자원을 줄이고 Tensor Core 연산을 지속시키기

실제 kernel은 register·shared memory·cache에 데이터 재사용을 늘리고 HBM 왕복과 register spill을 줄이는 방향으로 설계한다.

---

## 8. Unified Memory

`cudaMallocManaged()`로 할당한 Unified Memory는 CPU와 GPU가 하나의 coherent address space처럼 접근하게 한다. 명시적 `cudaMemcpy`를 줄여 프로그래밍은 단순해진다.

하지만 필요한 page가 현재 CPU 쪽에 있는데 GPU kernel이 접근하면 page fault가 발생하고, runtime이 해당 page를 GPU 쪽으로 migration하는 동안 kernel이 멈출 수 있다. PCIe 기반 시스템에서는 특히 이 비용이 클 수 있다. Grace Hopper/Blackwell의 NVLink-C2C는 CPU-GPU 사이 대역폭을 크게 높이지만 migration latency 자체가 사라지는 것은 아니다.

### 예측 가능한 이동으로 바꾸기

```cpp
cudaMemPrefetchAsync(ptr, bytes, gpuId, stream);
cudaMemAdvise(ptr, bytes, cudaMemAdviseSetPreferredLocation, gpuId);
cudaMemAdvise(ptr, bytes, cudaMemAdviseSetReadMostly, gpuId);
```

- `cudaMemPrefetchAsync`: kernel 전에 데이터를 target GPU/CPU로 미리 이동한다.
- `PreferredLocation`: 주로 사용할 위치를 driver에 알린다.
- `ReadMostly`: 주로 읽는 데이터임을 알린다.
- `SetAccessedBy`: 다른 GPU가 접근할 수 있음을 미리 알릴 수 있다.
- `cudaStreamAttachMemAsync`: 특정 stream에 memory 범위를 붙여 예기치 않은 cross-stream stall을 줄인다.

Unified Memory를 쓴다면 "페이지가 필요해진 뒤 이동"이 아니라 "필요해지기 전에 비동기로 이동"하도록 관리해야 한다.

---

## 9. Occupancy와 GPU 활용률

**occupancy**는 SM이 수용할 수 있는 최대 active warp 대비 현재 resident active warp의 비율이다.

```text
occupancy = active warps / maximum resident warps
```

한 warp가 HBM load를 기다릴 때 다른 ready warp가 실행되면 SM pipeline이 놀지 않는다. 이것이 occupancy가 memory latency를 숨기는 방식이다.

### occupancy를 낮추는 요소

- grid가 너무 작아 SM 전체에 충분한 block을 공급하지 못함
- block 크기가 warp 크기의 배수가 아님
- thread당 register 사용량이 많음
- block당 shared memory 사용량이 많음
- block 수/warp 수의 하드웨어 상한에 도달함

### 높을수록 항상 빠른 것은 아니다

occupancy를 강제로 100%에 맞추면 register를 적게 쓰게 되어 spill이 생기거나, thread 하나가 할 수 있는 instruction-level parallelism(ILP)이 줄 수 있다. memory bandwidth가 이미 포화됐다면 warp를 더 추가해도 빨라지지 않는다.

따라서 목표는 최대 occupancy 자체가 아니라, latency를 숨기기에 충분한 warp와 좋은 register/shared-memory 균형을 찾는 것이다. 실제 성능은 kernel 실행 시간, achieved occupancy, register spill, memory bandwidth를 같이 보고 판단한다.

### 병렬화가 부족한 코드

GPU tensor를 Python `for` loop에서 원소 하나씩 처리하면 수많은 작은 kernel이 순차 launch되어 GPU를 scalar processor처럼 쓰게 된다.

```python
# 비효율적: 원소마다 작은 GPU 연산을 순차 launch
for i in range(N):
    C[i] = A[i] + B[i]

# 일반적으로 적절함: 하나의 vectorized kernel이 전체 원소를 병렬 처리
C = A + B
```

PyTorch에서는 가능한 한 vectorized tensor operation과 compiler가 생성하는 fused/optimized kernel을 이용하는 편이 낫다.

### launch bounds와 Occupancy API

`__launch_bounds__(maxThreadsPerBlock, minBlocksPerSM)`는 compiler에 block 크기와 원하는 resident block 수의 힌트를 준다. compiler의 register allocation, unrolling, inlining 선택에 영향을 주어 occupancy를 높일 수 있다.

```cpp
__global__ __launch_bounds__(256, 4)
void myKernel(...) { /* ... */ }
```

이 값은 하드웨어 한계를 넘길 수 없다. 지나치게 낮은 register 제한은 spill을 만들 수 있으므로 profiler로 확인한다.

`cudaOccupancyMaxPotentialBlockSize()`는 kernel의 register/shared-memory 사용량을 고려해 occupancy가 높은 block size 후보와 최소 grid size를 계산한다. 다만 API의 추천값은 시작점이다. 실제로는 그 값과 주변 후보를 측정해 L2 동작, register pressure, 실행 시간을 비교해야 한다.

---

## 10. CUDA 정확성 점검: Compute Sanitizer

GPU kernel은 많은 thread가 동시에 실행되므로, out-of-bounds 접근이나 race가 즉시 명확하게 보이지 않을 수 있다. NVIDIA Compute Sanitizer는 runtime instrumentation으로 이런 오류를 찾는다.

```bash
compute-sanitizer --tool memcheck ./my_cuda_app
```

주요 도구는 다음과 같다.

- `memcheck`: global/local/shared memory의 범위 밖 접근, 정렬 오류, device-side leak
- `racecheck`: shared memory의 WAR/WAW/RAW race
- `initcheck`: 초기화되지 않은 device global memory 읽기
- `synccheck`: 잘못된 barrier와 동기화 사용

CI에서 `--error-exitcode`를 사용하고 NVTX 영역·kernel filter를 결합하면, 성능 측정 전에 correctness 회귀를 잡을 수 있다.

---

## 11. Roofline 모델: compute-bound인가 memory-bound인가

roofline은 kernel 성능의 상한을 두 가지로 나타낸다.

- 수평선: GPU의 최대 연산 성능(peak FLOPS)
- 대각선: 메모리 대역폭 × arithmetic intensity

**arithmetic intensity(AI)**는 HBM에서 옮긴 byte당 수행한 FLOP 수다.

```text
AI = FLOPs / bytes transferred

예: FP32 두 개를 읽어 더하고 결과 하나를 쓴다
읽기 8 B + 쓰기 4 B, 연산 1 FLOP
AI = 1 / 12 ≈ 0.083 FLOP/B
```

두 선이 만나는 ridge point보다 AI가 낮으면 memory-bound, 높으면 compute-bound에 가깝다.

```text
예상 성능 ≤ min(peak FLOPS, memory bandwidth × AI)
```

### memory-bound일 때의 방향

메모리 대역폭 사용률은 높고 ALU/Tensor Core 사용률이 낮다면, 더 많은 FLOP를 위한 thread만 추가하는 것보다 byte 이동을 줄여야 한다.

- register/shared/L2에서 데이터 재사용을 늘린다.
- global memory 접근을 coalesced하게 만든다.
- kernel fusion으로 중간 결과의 HBM 왕복을 줄인다.
- 가능한 경우 FP32 대신 FP16/FP8/FP4 등 낮은 정밀도를 사용한다.
- 압축·hardware decompression을 사용해 이동 byte를 줄인다.

LLM도 단계별로 성격이 다르다. prefill의 attention은 연산 제한인 경우가 많고, decode는 큰 weight/KV 데이터를 반복해서 읽어 메모리 제한이 되기 쉽다.

### profiler로 확인하기

- **Nsight Compute**: kernel별 DRAM bandwidth, cache hit rate, warp stall, achieved FLOPS, register 사용량
- **Nsight Systems**: CPU 작업, H2D/D2H 복사, kernel, GPU idle gap이 시간상 어떻게 겹치는지

`cudaMemcpyAsync`가 kernel과 실제로 overlap하려면 source/destination과 stream 의존성이 올바르고, host source인 경우 pinned memory가 필요하다. 타임라인에서 copy와 compute가 순차로만 보이면 default stream 동기화나 page-locked memory 부재 등을 점검한다.

---

## 핵심 정리

1. GPU는 32 thread warp를 많이 동시에 유지해 memory·pipeline 지연 시간을 숨기는 처리량 중심 프로세서다.
2. block 크기는 우선 32의 배수로 두고, 256을 시작 후보로 삼아 register/shared-memory 사용량과 함께 측정한다.
3. occupancy는 중요하지만 목표 자체가 아니다. 충분한 latency hiding과 register spill 방지 사이의 균형이 핵심이다.
4. `cudaMallocAsync`/`cudaFreeAsync`와 memory pool은 반복 할당의 전역 동기화와 overhead를 줄인다.
5. register → shared/L1 → L2 → HBM의 계층을 이해하고, 데이터 재사용·coalesced access·spill 감소로 HBM 접근을 줄인다.
6. Unified Memory는 편하지만 on-demand migration이 kernel을 멈출 수 있으므로 prefetch와 memory advice를 사용한다.
7. Roofline의 AI(FLOP/byte)로 memory-bound와 compute-bound를 구분하고, profiler로 실제 병목을 검증한다.
