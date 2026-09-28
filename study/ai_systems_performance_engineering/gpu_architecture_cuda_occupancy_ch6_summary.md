# Chapter 6. GPU Architecture, CUDA Programming, and Maximizing Occupancy

> 출처: Chris Fregly, *AI Systems Performance Engineering*\
> 범위: Chapter 6 --- GPU Architecture, CUDA Programming, and Maximizing
> Occupancy\
> 목적: GPU가 thread를 어떻게 실행하고 memory를 어떻게 사용하는지 이해한
> 뒤, CUDA kernel의 occupancy와 실제 throughput을 높인다.

## 0. 이 장의 핵심 흐름

Chapter 5가 "GPU에 데이터를 어떻게 계속 공급할 것인가"였다면 Chapter 6은
**GPU 내부에서 그 데이터를 어떻게 병렬로 처리하는가**를 다룬다.

``` text
CPU
 ↓ kernel launch
GPU
 ↓
Grid
 ↓
Thread Blocks
 ↓
Warps
 ↓
Threads
 ↓
SM에서 실행
```

성능을 결정하는 핵심은 단순히 thread를 많이 만드는 것이 아니다.

``` text
충분한 parallelism
+ 적절한 block size
+ register/shared memory 사용량
+ 높은 latency hiding
+ 효율적인 memory hierarchy 사용
+ workload의 compute/memory 특성 파악
```

------------------------------------------------------------------------

## 1. CPU와 GPU의 설계 목표 차이

CPU는 상대적으로 적은 수의 강력한 core로 single-thread latency를 줄이는
데 초점을 둔다.

GPU는 매우 많은 thread를 동시에 실행하여 **throughput**을 높이는 데
초점을 둔다.

``` text
CPU
→ 적은 수의 복잡한 core
→ 한 작업을 빠르게

GPU
→ 많은 parallel execution resource
→ 수천~수만 thread를 동시에
```

GPU에서는 어떤 thread/warp가 memory를 기다리는 동안 다른 warp를 실행해
latency를 숨긴다.

이를 **latency hiding**이라고 한다.

------------------------------------------------------------------------

## 2. Streaming Multiprocessor (SM)

GPU는 여러 개의 SM으로 구성된다.

``` text
GPU
├─ SM 0
├─ SM 1
├─ SM 2
├─ ...
└─ SM N
```

SM은 GPU에서 thread/warp가 실제로 실행되는 핵심 단위다.

SM 내부에는 대략 다음 자원이 있다.

``` text
Warp schedulers
FP / INT execution units
Tensor Cores
Load / Store units
Special Function Units
Registers
Shared Memory / L1
TMEM
```

Blackwell 기준으로 책은 SM 하나가 최대 64 warps, 즉 2,048 threads를
resident 상태로 추적할 수 있다고 설명한다.

``` text
64 warps × 32 threads = 2,048 threads
```

------------------------------------------------------------------------

## 3. SIMT: Single Instruction, Multiple Threads

NVIDIA GPU는 SIMT execution model을 사용한다.

핵심 실행 단위는 **warp**다.

``` text
1 Warp = 32 Threads
```

한 warp의 32개 thread는 기본적으로 같은 instruction을 함께 실행한다.

``` text
Warp
├─ Thread 0
├─ Thread 1
├─ ...
└─ Thread 31

같은 instruction
각자 다른 data
```

예를 들어 배열의 각 원소에 2를 곱한다면 32개 thread가 서로 다른 원소를
동시에 처리할 수 있다.

------------------------------------------------------------------------

## 4. Warp Divergence

같은 warp 안에서 thread들이 서로 다른 branch를 선택하면 문제가 생긴다.

``` cpp
if (condition) {
    A();
} else {
    B();
}
```

예:

``` text
Thread 0~15 → A
Thread 16~31 → B
```

warp 전체가 완전히 독립적으로 A와 B를 동시에 실행하는 것이 아니라,
필요한 lane을 mask하면서 branch 경로를 나눠 실행해야 한다.

따라서 branch가 갈라질수록 실행 효율이 떨어질 수 있다.

중요:

``` text
같은 warp 내부의 divergence → 문제 가능
서로 다른 warp가 다른 branch → 동일한 의미의 divergence penalty 아님
```

Chapter 8에서 warp divergence를 더 깊게 다룬다.

------------------------------------------------------------------------

## 5. Thread → Warp → Block → Grid

CUDA thread hierarchy:

``` text
Grid
 ├─ Block 0
 │   ├─ Warp 0 → 32 threads
 │   ├─ Warp 1 → 32 threads
 │   └─ ...
 ├─ Block 1
 └─ ...
```

### Thread

가장 작은 logical execution unit이다.

각 thread는 자신의:

``` text
threadIdx
registers
local state
```

를 가진다.

### Warp

32개 thread를 묶은 실제 SIMT scheduling 단위다.

### Thread Block

여러 thread의 그룹이다.

block 안의 thread는 shared memory를 공유하고 `__syncthreads()` 같은
barrier로 동기화할 수 있다.

### Grid

하나의 kernel launch가 생성하는 모든 block의 집합이다.

------------------------------------------------------------------------

## 6. 왜 block size는 32의 배수인가?

warp가 32 thread이기 때문이다.

예:

``` text
256 threads/block
= 8 full warps
```

반면:

``` text
33 threads/block
= Warp 0: 32 threads 사용
= Warp 1: 1 thread 사용 + 31 lane 낭비
```

두 번째 warp도 scheduler resource를 차지하기 때문에 비효율적이다.

따라서 일반적으로 block size를 32의 배수로 선택한다.

책은 256 threads/block을 흔한 시작점으로 제시하고, workload에 따라
128/256/512 등을 profiling으로 조정한다.

------------------------------------------------------------------------

## 7. Blackwell의 주요 thread/block limit

책에서 제시하는 Blackwell B200 기준:

``` text
Warp size                     = 32 threads
Max threads / block           = 1,024
Max warps / block             = 32
Max resident warps / SM       = 64
Max resident threads / SM     = 2,048
Max active blocks / SM        = 32
```

이 제한은 occupancy 계산에 직접 영향을 준다.

예:

``` text
Block = 1,024 threads
→ SM당 최대 2 blocks만 thread 수 기준으로 resident 가능

Block = 256 threads
→ thread 수 기준 최대 8 blocks 가능
```

하지만 실제 resident block 수는 register와 shared memory 사용량 때문에
더 줄어들 수 있다.

------------------------------------------------------------------------

## 8. CUDA Kernel 기본 구조

GPU에서 실행되는 함수에는 `__global__`을 붙인다.

``` cpp
__global__ void myKernel(float* input, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < N) {
        input[idx] *= 2.0f;
    }
}
```

kernel launch:

``` cpp
myKernel<<<blocksPerGrid, threadsPerBlock>>>(input, N);
```

여기서:

``` text
threadsPerBlock
= block 하나에 몇 thread를 만들 것인가

blocksPerGrid
= 전체 grid에 몇 block을 만들 것인가
```

------------------------------------------------------------------------

## 9. Global Thread Index

1D array를 처리할 때 흔히:

``` cpp
int idx = blockIdx.x * blockDim.x + threadIdx.x;
```

를 사용한다.

예:

``` text
blockDim.x = 256

Block 0
threadIdx 0~255
→ idx 0~255

Block 1
threadIdx 0~255
→ idx 256~511
```

이 방식으로 각 thread가 서로 다른 element를 담당한다.

------------------------------------------------------------------------

## 10. Bounds Check

N이 block size의 정확한 배수가 아닐 수 있다.

``` text
N = 1000
threadsPerBlock = 256

4 blocks × 256 = 1024 threads
```

24개의 extra thread가 생긴다.

따라서:

``` cpp
if (idx < N)
```

를 넣어 array 범위를 넘어가지 않게 한다.

CUDA kernel의 illegal memory access 같은 오류는 kernel 내부 thread에서
일반 CPU exception처럼 즉시 나타나지 않고 이후 synchronization/API 호출
시 드러날 수 있으므로 kernel launch 뒤 error check와 synchronization이
debugging에 중요하다.

------------------------------------------------------------------------

## 11. blocksPerGrid 계산

보편적인 식:

``` cpp
blocksPerGrid =
    (N + threadsPerBlock - 1) / threadsPerBlock;
```

이는 integer division을 이용한 ceiling 계산이다.

예:

``` text
N = 1,000,000
threadsPerBlock = 256

blocksPerGrid = 3,907
```

마지막 block에 일부 unused thread가 생기더라도 bounds check로 안전하게
처리한다.

------------------------------------------------------------------------

## 12. 2D / 3D Kernel

이미지나 matrix는 2D grid/block으로 자연스럽게 표현할 수 있다.

``` cpp
dim3 threadsPerBlock(16, 16);
```

``` text
16 × 16 = 256 threads
```

thread coordinate:

``` cpp
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;
```

3D volume도 `dim3(x, y, z)`를 이용해 같은 방식으로 확장할 수 있다.

------------------------------------------------------------------------

## 13. CUDA Forward / Backward Compatibility

CUDA binary에는 GPU가 직접 실행하는 architecture-specific code와 PTX
같은 intermediate representation을 포함할 수 있다.

책의 핵심 권고는 미래 GPU에서도 실행될 수 있도록 PTX를 포함하는 것이다.

``` text
현재 GPU용 cubin/SASS
+
PTX
```

PTX가 있으면 새로운 GPU에서 driver가 JIT compile할 수 있다.

`CUDA_FORCE_PTX_JIT=1`을 사용하면 PTX JIT 경로가 실제로 동작하는지
확인할 수 있다.

새 hardware 전용 optimization을 사용한다면 generation-specific target과
함께 fallback path도 고려한다.

------------------------------------------------------------------------

## 14. Synchronous Allocation의 비용

전통적인:

``` cpp
cudaMalloc()
cudaFree()
```

는 상대적으로 비싼 operation이다.

memory allocation/free 과정에서 synchronization과 driver/OS interaction
비용이 발생할 수 있다.

반복적으로 allocation/free하면 kernel 자체보다 allocator overhead가 커질
수도 있다.

------------------------------------------------------------------------

## 15. `cudaMallocAsync` / `cudaFreeAsync`

책은 stream-ordered asynchronous allocation을 권장한다.

``` cpp
cudaMallocAsync(..., stream);
cudaFreeAsync(..., stream);
```

CUDA runtime은 memory pool을 활용해 해제된 GPU memory를 재사용할 수
있다.

``` text
cudaMallocAsync
      ↓
CUDA Memory Pool
      ↓
reuse
      ↓
cudaFreeAsync
```

매번 OS-level allocation을 새로 수행하는 비용을 줄이고 불필요한 global
synchronization도 피할 수 있다.

PyTorch의 caching allocator도 비슷한 목적을 가진다.

------------------------------------------------------------------------

# 16. GPU Memory Hierarchy

GPU memory는 모두 같은 속도가 아니다.

책의 큰 계층:

``` text
빠름 / 작음
↑
Registers
Shared Memory / L1
TMEM
Constant Cache
L2
Local Memory (spill)
Global Memory / HBM
Host Memory
↓
느림 / 큼
```

성능 최적화의 중요한 원칙은 **자주 사용하는 데이터를 가능한 한 빠른
on-chip memory에서 재사용하는 것**이다.

------------------------------------------------------------------------

## 17. Registers

register는 thread의 local variable을 저장하는 매우 빠른 on-chip
memory다.

Blackwell 기준 책의 설명:

``` text
64K × 32-bit registers / SM
최대 255 registers / thread
```

register access는 매우 빠르지만 무한하지 않다.

thread 하나가 너무 많은 register를 요구하면 **register pressure**가
증가한다.

더 심하면 register 값 일부가 local memory로 spill된다.

``` text
Registers 부족
      ↓
Register Spill
      ↓
Local Memory
      ↓
실제로는 off-chip DRAM/HBM
      ↓
latency 크게 증가
```

또한 register를 많이 쓰면 한 SM에 동시에 resident할 수 있는 thread/warp
수가 줄어 occupancy가 낮아질 수 있다.

------------------------------------------------------------------------

## 18. Shared Memory / L1

shared memory는 같은 block의 thread들이 공유하는 on-chip memory다.

``` text
Thread Block
 ├─ Thread 0 ─┐
 ├─ Thread 1 ─┤
 ├─ ...       ├→ Shared Memory
 └─ Thread N ─┘
```

global memory에서 같은 데이터를 반복해서 가져오는 대신 한 번 shared
memory에 올리고 여러 thread가 재사용할 수 있다.

Blackwell에서는 L1/data cache와 shared-memory resource가 같은 on-SM SRAM
영역을 공유하며 carveout을 조절할 수 있다.

shared memory는 빠르지만 block당 사용량이 커질수록 동시에 resident
가능한 block 수가 줄어 occupancy를 제한할 수 있다.

------------------------------------------------------------------------

## 19. TMEM

Blackwell에는 Tensor Core operation을 위한 **Tensor Memory(TMEM)**가
있다.

일반 CUDA pointer로 직접 사용하는 보통 memory와는 다르며 Tensor Core
operation의 accumulator 등에 사용된다.

책에서는 TMA(Tensor Memory Accelerator)가 global/shared/TMEM 사이의 data
movement를 orchestration하는 구조를 설명한다.

``` text
Global Memory
     ↓
    TMA
     ↓
Shared Memory
     ↓
Tensor Core
     ↕
    TMEM
```

목표는 data movement를 효율화하여 Tensor Core가 실제 matrix compute에
집중하도록 하는 것이다.

------------------------------------------------------------------------

## 20. Constant Memory Cache

작고 read-only이며 많은 thread가 동일한 값을 읽는 데이터에 적합하다.

예:

``` text
lookup table
RoPE 관련 값
ALiBi slope
LayerNorm parameter
quantization scale
```

warp의 32개 thread가 같은 address를 읽으면 broadcast 형태로 매우
효율적으로 전달할 수 있다.

반대로 thread마다 서로 다른 constant address를 읽으면 access가
serialize될 수 있다.

------------------------------------------------------------------------

## 21. L2 Cache

L2는 GPU 전체 SM이 공유하는 cache다.

``` text
SM 0 ─┐
SM 1 ─┤
SM 2 ─┼→ L2 → HBM
...   ─┘
```

어떤 block이 읽은 data를 다른 block이 다시 사용할 수 있다면 HBM까지 다시
내려가는 것을 줄일 수 있다.

책은 global load를 aligned/coalesced 형태로 구성해 L2와 DRAM bandwidth를
효율적으로 사용하는 것을 강조한다.

------------------------------------------------------------------------

## 22. Global Memory / HBM

HBM은 GPU의 큰 device memory다.

용량과 bandwidth는 매우 크지만 on-chip register/shared memory보다
latency가 훨씬 높다.

따라서:

``` text
HBM에서 매번 읽음
      ↓
memory latency / bandwidth 부담
```

보다:

``` text
HBM에서 한 번 읽음
      ↓
L2 / L1 / Shared / Register
      ↓
여러 번 reuse
```

가 효율적이다.

Chapter 7에서 이 memory access pattern을 더 깊게 다룬다.

------------------------------------------------------------------------

## 23. Unified Memory

CUDA Managed Memory는 CPU와 GPU에서 사용할 memory를 하나의
abstraction으로 다룰 수 있게 한다.

편리하지만 실제 data가 필요한 processor 쪽으로 page migration이 발생할
수 있다.

``` text
CPU에서 page 사용
       ↓
GPU에서 접근
       ↓
page migration
       ↓
unexpected stall 가능
```

따라서 책은 `cudaMemPrefetchAsync`와 memory advice 등을 이용해 data
placement를 미리 관리하는 방법을 설명한다.

------------------------------------------------------------------------

# 24. Occupancy란?

Occupancy는 간단히 말하면 **SM이 동시에 유지할 수 있는 최대 warp 수 대비
실제 active warp 수의 비율**이다.

``` text
Occupancy
= Active Warps / Maximum Resident Warps
```

Blackwell에서 최대 64 warp/SM이라고 하면:

``` text
32 active warps
→ occupancy 50%

64 active warps
→ occupancy 100%
```

occupancy가 중요한 이유는 latency hiding이다.

``` text
Warp A → memory 기다림
Warp B → 실행
Warp C → 실행
Warp D → 실행
```

ready warp가 충분하면 한 warp가 기다려도 SM이 놀지 않는다.

------------------------------------------------------------------------

## 25. Occupancy를 제한하는 자원

단순히 thread를 많이 launch한다고 occupancy가 올라가는 것은 아니다.

대표 제한 요소:

``` text
Threads / SM
Warps / SM
Blocks / SM
Registers / SM
Shared Memory / SM
```

예를 들어 block 하나가 shared memory를 너무 많이 사용하면 SM에 block
여러 개를 동시에 올릴 수 없다.

``` text
SM Shared Memory
┌─────────────────────┐
│ Block A가 대부분 사용 │
└─────────────────────┘

→ Block B를 동시에 resident 못함
→ active warp 감소
→ occupancy 감소
```

register도 마찬가지다.

``` text
registers/thread ↑
       ↓
한 SM에 resident 가능한 threads ↓
       ↓
occupancy ↓
```

------------------------------------------------------------------------

## 26. 높은 Occupancy가 항상 최고 성능은 아니다

이 장에서 매우 중요한 부분이다.

``` text
Occupancy 100%
≠ 항상 최고 throughput
```

occupancy는 latency hiding을 위한 수단이다.

kernel이 이미 충분한 instruction-level parallelism을 가지고 있거나 다른
resource가 병목이라면 moderate occupancy에서도 높은 성능이 나올 수 있다.

반대로 occupancy를 억지로 높이려고 thread당 register 수를 너무 줄이면
register spill이 발생하여 오히려 느려질 수 있다.

``` text
Occupancy 올리려고 register 제한
           ↓
register spill
           ↓
HBM/local memory access 증가
           ↓
성능 하락
```

따라서 목표는 occupancy 숫자 최대화가 아니라 **실제 kernel throughput
최대화**다.

------------------------------------------------------------------------

## 27. Launch Bounds

CUDA의 `__launch_bounds__`를 이용하면 compiler에게 kernel의 launch
조건을 알려 register allocation 등의 optimization에 힌트를 줄 수 있다.

개념적으로:

``` text
이 kernel은
block당 최대 몇 thread를 사용할 것이고
SM당 최소 몇 block이 resident해야 한다
```

라는 정보를 compiler에게 제공한다.

compiler는 이를 이용해 register usage와 occupancy 사이의 trade-off를
조절할 수 있다.

하지만 launch bounds를 무리하게 사용하면 register pressure/spill이 생길
수 있으므로 profiling으로 검증해야 한다.

------------------------------------------------------------------------

## 28. Functional Correctness: Compute Sanitizer

성능을 최적화하기 전에 kernel이 정확해야 한다.

CUDA의 asynchronous execution 특성 때문에 illegal memory access나 race
condition이 즉시 눈에 띄지 않을 수 있다.

NVIDIA Compute Sanitizer를 이용해 다음 종류의 문제를 찾을 수 있다.

``` text
invalid memory access
race condition
uninitialized memory
synchronization problem
```

성능 tuning 전에 correctness를 확인하는 것이 중요하다.

------------------------------------------------------------------------

# 29. Roofline Model

Roofline model은 kernel이 왜 느린지를 크게 두 종류로 나누는 도구다.

``` text
Compute-bound
vs
Memory-bound
```

핵심 개념은 **Arithmetic Intensity**다.

``` text
Arithmetic Intensity
= 수행한 FLOPs / memory에서 이동한 bytes
```

### Arithmetic Intensity가 낮음

``` text
memory에서 data 많이 가져옴
계산은 조금 함
```

→ memory-bound 가능성이 높다.

### Arithmetic Intensity가 높음

``` text
data를 한 번 가져온 뒤
계산을 많이 함
```

→ compute-bound 방향으로 간다.

------------------------------------------------------------------------

## 30. Roofline을 직관적으로 보기

``` text
Performance
  ^
  |                   ───────── Compute Ceiling
  |                 /
  |               /
  |             /
  |           /
  |         /
  |_______/____________________________> Arithmetic Intensity
       Memory-bound       Compute-bound
```

왼쪽 영역에서는 memory bandwidth가 성능을 제한한다.

오른쪽에서는 GPU의 compute throughput이 제한한다.

------------------------------------------------------------------------

## 31. Memory-bound Kernel 최적화 방향

memory-bound라면 단순히 CUDA core를 더 바쁘게 만들려고 해도 효과가 작다.

대신:

``` text
memory traffic 감소
data reuse 증가
coalesced access
register/shared memory 활용
precision 감소
prefetch / overlap
```

등이 중요하다.

FP32 대신 FP16/FP8/FP4처럼 더 작은 data type을 사용할 수 있으면 같은
memory bandwidth로 더 많은 element를 이동할 수 있어 arithmetic intensity
관점에서도 유리할 수 있다.

------------------------------------------------------------------------

## 32. Compute-bound Kernel 최적화 방향

compute-bound라면 memory bandwidth보다 연산 자원이 제한 요소다.

따라서:

``` text
Tensor Core 활용
lower precision
instruction efficiency
parallelism
ILP
kernel fusion / algorithmic optimization
```

같은 방향을 본다.

책은 Nsight Compute의 per-kernel metric과 Nsight Systems timeline을
사용해 실제 병목을 구분하라고 강조한다.

------------------------------------------------------------------------

## 33. Chapter 6 전체 연결

``` text
CPU
 │
 │ Kernel Launch
 ▼
Grid
 │
 ├─ Block
 │   ├─ Warp (32 threads)
 │   ├─ Warp
 │   └─ ...
 │
 ▼
SM
 │
 ├─ Warp Scheduler
 ├─ Registers
 ├─ Shared/L1
 ├─ Tensor Cores
 └─ TMEM
 │
 ▼
L2
 │
 ▼
HBM
```

성능 관점:

``` text
Block size 선택
      ↓
Warp가 충분히 차는가?
      ↓
Register / Shared Memory가 너무 많은가?
      ↓
몇 개 warp가 동시에 resident 가능한가?
      ↓
Occupancy / Latency Hiding
      ↓
실제 kernel throughput
      ↓
Roofline으로 memory-bound / compute-bound 판별
      ↓
병목에 맞는 최적화
```

------------------------------------------------------------------------

## 34. Chapter 5와 Chapter 6 연결

Chapter 5:

``` text
Storage → GPU까지 데이터를 빨리 공급
```

Chapter 6:

``` text
도착한 데이터를 GPU 내부에서 효율적으로 처리
```

즉:

``` text
Storage
  ↓         Chapter 5
GPU HBM
  ↓
L2
  ↓
Shared / L1
  ↓         Chapter 6
Registers
  ↓
CUDA Core / Tensor Core
```

Chapter 5가 느리면 GPU가 굶고, Chapter 6이 비효율적이면 데이터가
도착해도 GPU hardware를 제대로 활용하지 못한다.

------------------------------------------------------------------------

## Key Takeaways

1.  GPU는 single-thread latency보다 massive parallel throughput을 위해
    설계됐다.
2.  SM이 thread 실행의 핵심 hardware 단위이며 warp scheduler가 ready
    warp를 골라 실행한다.
3.  CUDA의 기본 실행 계층은 `thread → warp → block → grid`다.
4.  warp는 32 thread이므로 block size는 일반적으로 32의 배수로 잡는다.
5.  256 threads/block은 흔한 시작점이지만 최적값은
    register/shared-memory 사용량과 profiling 결과에 따라 달라진다.
6.  `cudaMallocAsync`/`cudaFreeAsync`와 memory pool은 allocation
    overhead와 synchronization을 줄이는 데 도움이 된다.
7.  memory hierarchy는 대략 `register → shared/L1 → L2 → HBM → host`이며
    빠른 계층에서 data reuse를 높이는 것이 중요하다.
8.  register pressure가 너무 높으면 occupancy가 감소하거나 spill이
    발생할 수 있다.
9.  shared memory 사용량 역시 동시에 resident 가능한 block 수를
    제한한다.
10. occupancy는 latency hiding에 중요하지만 100% occupancy 자체가 목표는
    아니다.
11. launch bounds는 compiler의 register/occupancy trade-off에 힌트를 줄
    수 있지만 실제 benchmark가 필요하다.
12. Unified Memory는 편리하지만 예상치 못한 page migration stall을 만들
    수 있어 prefetch/advice가 중요하다.
13. Roofline model의 핵심은 arithmetic intensity이며 kernel이
    memory-bound인지 compute-bound인지 구분하는 데 사용한다.
14. Nsight Compute와 Nsight Systems를 통해 이론적인 occupancy보다 실제
    bottleneck과 throughput을 측정해야 한다.
