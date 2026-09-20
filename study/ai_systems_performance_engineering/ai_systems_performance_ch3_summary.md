# Chapter 3 — OS, Docker, and Kubernetes Tuning for GPU-Based Environments
> Source: *AI Systems Performance Engineering* — Chris Fregly
> 범위: Chapter 3

---

# 1. Chapter 3 핵심 주제

아무리 GPU 자체 성능이 좋아도 주변 시스템이 느리면 GPU는 기다리게 된다.

Chapter 3의 핵심은 다음이다.

> **GPU가 놀지 않도록 OS, CPU, 메모리, 드라이버, 컨테이너, Kubernetes까지 함께 튜닝한다.**

주요 범위:

- Linux OS
- NVIDIA Driver / CUDA Runtime
- NUMA
- CPU / Memory Pinning
- Hugepages
- Scheduler / IRQ Affinity
- Swap / Filesystem / CPU Frequency
- Persistence Mode
- MPS
- MIG
- GPU Clock / ECC
- GPU Memory Fragmentation / OOM
- Docker / NVIDIA Container Toolkit
- Kubernetes Topology Manager
- SLURM
- RDMA / Host Networking
- Resource Isolation

최종 목표는 Chapter 1과 동일하게 **Goodput 증가**다.

---

# 2. GPU Software Stack

GPU 프로그램은 PyTorch 코드가 바로 GPU에 실행되는 구조가 아니다.

```text
PyTorch / TensorFlow / JAX
          ↓
CUDA Libraries
cuBLAS / cuDNN / NCCL
          ↓
CUDA Runtime
          ↓
NVIDIA GPU Driver
          ↓
GPU Hardware
```

PyTorch의 고수준 연산도 내부적으로 CUDA runtime과 최적화 라이브러리로 내려간다.
따라서 성능을 분석할 때는 모델 코드뿐 아니라 **전체 software stack**을 봐야 한다.

---

# 3. NVIDIA GPU Driver

GPU Driver는 Linux와 GPU 사이의 가장 낮은 소프트웨어 계층이다.

주요 역할:

- GPU memory allocation
- GPU task scheduling
- GPU partitioning
- hardware feature control

대표 도구:

```bash
nvidia-smi
```

확인 가능한 항목:

- GPU utilization
- temperature
- memory usage
- ECC status
- power
- clocks
- persistence mode

최신 GPU와 CUDA 기능을 제대로 사용하려면 지원되는 최신 driver를 사용하는 것이 중요하다.

---

# 4. CUDA Toolkit / Runtime

CUDA Toolkit에는 다음이 포함된다.

- `nvcc`
- CUDA Runtime (`cudart`)
- cuBLAS
- cuDNN
- NCCL
- 기타 CUDA libraries

```text
CUDA Program
    ↓
CUDA Runtime
    ↓
GPU Driver
    ↓
GPU
```

---

# 5. PTX / CUBIN / Fatbinary

## PTX

```text
PTX = Intermediate Representation
```

새로운 GPU에서 driver가 JIT compile할 수 있어 **forward compatibility**에 유리하다.

## CUBIN

```text
CUBIN = 특정 GPU architecture용 SASS binary
```

현재 architecture에서 바로 실행할 수 있지만 미래 GPU에 대한 forward compatibility는 없다.

## Fatbinary

```text
Fatbinary
├─ CUBIN / SASS
└─ PTX
```

현재 GPU에서는 최적화된 binary를 사용하고, 미래 GPU에서는 PTX를 JIT compile하도록 구성할 수 있다.

---

# 6. Python GPU Programming

책에서 언급하는 Python 계열 GPU 도구:

- CUDA Python
- cuPy
- cuPyNumeric
- cuTile
- NVIDIA Warp
- OpenAI Triton

특히 Triton은 Python 기반 DSL로 custom GPU kernel을 작성할 수 있으며, PyTorch compiler의 TorchInductor도 내부적으로 Triton을 활용한다.

---

# 7. PyTorch Compiler Stack

```text
PyTorch
  ↓
TorchDynamo
  ↓
AOT Autograd
  ↓
TorchInductor
  ↓
Triton / CUDA Kernel
  ↓
GPU
```

고수준 Python 코드는 결국 낮은 수준의 CUDA operation으로 내려간다.

---

# 8. 가장 흔한 병목: GPU가 CPU를 기다림

CPU가 다음 batch를 준비하지 못하면 GPU가 idle 상태가 된다.

CPU가 수행하는 대표 작업:

- disk에서 dataset 읽기
- tokenization
- augmentation
- preprocessing
- batch 생성
- kernel dispatch
- process / thread coordination

핵심 질문:

> **CPU가 GPU를 충분히 빠르게 먹여 살릴 수 있는가?**

---

# 9. NUMA

NUMA:

```text
Non-Uniform Memory Access
```

현대 서버는 CPU, RAM, GPU, NIC 등이 여러 NUMA node로 나뉠 수 있다.

```text
NUMA Node 0
├─ CPU Core 0~31
├─ RAM 0
├─ GPU 0~3
└─ NIC 0

NUMA Node 1
├─ CPU Core 32~63
├─ RAM 1
├─ GPU 4~7
└─ NIC 1
```

같은 NUMA node 안의 resource를 사용하는 것이 가장 빠르다.

책의 예:

```text
Local NUMA Memory Access  ≈ 80 ns
Remote NUMA Memory Access ≈ 139 ns
```

remote access가 약 75% 더 높은 latency를 보일 수 있다.

---

# 10. CPU Pinning

OS scheduler가 process를 다른 core나 다른 NUMA node로 이동시키면 GPU feeding latency가 증가할 수 있다.

그래서 특정 CPU / NUMA node에 process를 고정한다.

```bash
numactl --cpunodebind=1 --membind=1 \
  python train.py --gpu 4
```

또는 `taskset`, cgroups 등을 사용할 수 있다.

핵심:

```text
CPU affinity
+
Memory affinity
+
GPU locality
```

를 함께 고려해야 한다.

---

# 11. Memory Binding

CPU만 pinning해도 memory가 다른 NUMA node에 있다면 remote memory access가 발생한다.

따라서 memory allocation도 같은 NUMA node로 묶는다.

```bash
numactl \
  --cpunodebind=1 \
  --membind=1 \
  python train.py
```

> **CPU와 Memory를 같이 bind해야 NUMA 최적화가 완성된다.**

---

# 12. Grace Blackwell에서도 NUMA Locality는 중요

Grace Blackwell은 CPU와 GPU가 NVLink-C2C로 연결되어 있지만 Linux 관점에서는 CPU DRAM과 GPU HBM이 여전히 서로 다른 memory pool이다.

따라서 Grace 기반 시스템에서도 local CPU / local memory를 사용하는 것이 유리하다.

---

# 13. Pinned Memory

Pinned Memory:

```text
Pinned Memory
= Page-Locked Memory
= Nonpageable Memory
```

OS가 swap하거나 이동시키지 않는 host memory다.
GPU나 NIC가 DMA로 직접 접근하기 쉬워진다.

책에서는 pinned host memory → GPU transfer가 pageable memory보다 **2~3배 빠를 수 있다**고 설명한다.

PyTorch 예:

```python
DataLoader(
    dataset,
    pin_memory=True
)
```

GPU copy:

```python
batch = batch.to("cuda", non_blocking=True)
```

이를 조합하면 data loading과 GPU computation을 overlap할 수 있다.

책에서는 workload에 따라 `pin_memory=True`가 host-to-device 병목을 줄여 **10~20% 정도 개선되는 사례**가 있을 수 있다고 설명한다.

---

# 14. DataLoader 튜닝

```python
DataLoader(
    num_workers=...,
    pin_memory=True,
    persistent_workers=True,
    prefetch_factor=...
)
```

- `num_workers`: 병렬 data loading worker 수
- `pin_memory=True`: H2D transfer를 위한 pinned memory
- `persistent_workers=True`: epoch마다 worker 재생성 방지
- `prefetch_factor`: 다음 batch 미리 준비

목표:

> GPU가 현재 batch를 계산하는 동안 CPU는 다음 batch를 준비한다.

---

# 15. Hugepages / THP

기본 Linux memory page는 보통 4 KB이고 hugepage는 2 MB 같은 큰 page를 사용한다.

장점:

- page table entry 감소
- TLB miss 감소
- memory management overhead 감소

Transparent Huge Pages(THP)는 이를 자동으로 관리하지만 background compaction 때문에 pause가 생길 수 있다.

책의 방향:

```text
Training / throughput 중심
→ THP enable 고려

Latency-sensitive inference
→ THP disable 또는 madvise 고려
```

workload별 benchmark가 필요하다.

---

# 16. Scheduler / CPU Isolation

중요한 GPU feeding thread가 background process에 방해받지 않게 CPU core를 분리할 수 있다.

대표 방법:

```text
isolcpus
nohz_full
cgroup cpuset
cset
```

핵심:

> AI workload용 core와 OS/background process용 core를 분리한다.

---

# 17. IRQ Affinity

NIC나 GPU interrupt를 다른 NUMA node의 CPU가 처리하면 cross-node traffic과 cache disruption이 생길 수 있다.

이상적 구조:

```text
NIC / GPU
   ↓ IRQ
Local CPU
```

즉 IRQ도 local NUMA CPU에 bind하는 것이 좋다.

---

# 18. Swapping

GPU node의 host memory가 swap되면 GPU feeding latency가 크게 증가할 수 있다.

책에서는 GPU workload node에서 swap을 최소화하도록 설명한다.

예:

```text
vm.swappiness = 0
```

또는 swap disable을 고려할 수 있다.

---

# 19. Filesystem / CPU Frequency / Host Allocator

AI workload는 dataset read, model loading, checkpoint, logging 등 I/O가 많다.
따라서 filesystem read-ahead, write-back, storage configuration 등도 병목이 될 수 있다.

CPU는 power saving 때문에 frequency를 낮추거나 깊은 C-state에 들어갈 수 있다.
latency-sensitive workload에서는 `performance` governor 같은 설정을 고려할 수 있다.

또한 host-side memory allocation contention도 병목이 될 수 있으므로 GPU뿐 아니라 CPU allocator overhead도 profiling해야 한다.

---

# 20. GPU Persistence Mode

Persistence Mode는 GPU를 ready 상태로 유지해 cold-start overhead를 줄인다.

```bash
systemctl enable nvidia-persistenced
```

장점:

- CUDA cold start 감소
- initialization latency 감소
- interactive / latency-sensitive workload에 유리

단점:

- idle power consumption 약간 증가

중요:

> Persistence mode는 연산 자체를 빠르게 만드는 기능이 아니라 **startup overhead를 줄이는 기능**이다.

---

# 21. NVIDIA MPS

MPS:

```text
Multi-Process Service
```

기본적으로 여러 process가 하나의 GPU를 공유하면 time-slicing될 수 있다.
MPS는 여러 process의 kernel을 동시에 실행할 수 있게 해 idle gap을 줄인다.

```text
Process A ─┐
           ├─ GPU concurrent execution
Process B ─┘
```

특히 여러 작은 inference workload가 하나의 큰 GPU를 공유할 때 유용하다.

```text
MPS = Utilization Optimization
```

---

# 22. MIG

MIG:

```text
Multi-Instance GPU
```

하나의 physical GPU를 hardware-isolated partition으로 나눈다.

```text
Physical GPU
├─ MIG Instance 1
├─ MIG Instance 2
├─ MIG Instance 3
└─ ...
```

각 instance는 독립적인 SM, GPU memory, cache fraction, engine context 등을 할당받는다.

---

# 23. MIG vs MPS

| 기능 | MPS | MIG |
|---|---|---|
| 목적 | 동시 실행 | 하드웨어 partition |
| Isolation | 약함 | 강함 |
| Resource Guarantee | 제한적 | 명확함 |
| Flexible Sharing | 좋음 | fixed profile |
| 대표 활용 | 여러 작은 process | multi-tenant inference |

쉽게 말하면:

```text
MPS = GPU를 같이 사용
MIG = GPU를 잘라서 사용
```

---

# 24. Blackwell B200 MIG Profile 예

| MIG Profile | Memory Fraction | SM Fraction | GPU Memory |
|---|---:|---:|---:|
| `1g.23gb` | 1/8 | 1/7 | 23 GB |
| `1g.45gb` | 2/8 | 1/7 | 45 GB |
| `2g.45gb` | 2/8 | 2/7 | 45 GB |
| `3g.90gb` | 4/8 | 3/7 | 90 GB |
| `4g.90gb` | 4/8 | 4/7 | 90 GB |
| `7g.180gb` | Full | Full | 180 GB |

MIG profile은 arbitrary하게 만드는 것이 아니라 GPU generation별 fixed profile을 사용한다.

Large distributed training처럼 GPU 전체 compute와 fast interconnect를 활용해야 하는 workload에는 full GPU가 더 적합하다.

---

# 25. GPU Clock / Power Limit

NVIDIA GPU Boost는 power / thermal 상태에 따라 clock을 자동 조절한다.
일반 workload에서는 auto boost가 보통 적절하다.

하지만 benchmark에서는 clock 변화가 결과를 왜곡할 수 있다.

```bash
nvidia-smi -lgc <clock>
```

power limit도 설정할 수 있다.

```bash
nvidia-smi -pl <watts>
```

가능한 효과:

```text
Peak Power ↓
Temperature ↓
Thermal Throttling ↓
Performance/Watt ↑
```

benchmark에서는 clock, temperature, power를 함께 통제해야 한다.

---

# 26. ECC

ECC:

```text
Error Correcting Code
```

GPU memory bit error를 감지 / 수정한다.
Data Center GPU에서는 일반적으로 ECC를 켜두는 것이 권장된다.

이유:

```text
Memory Error
 ↓
Training Crash
또는
Silent Model Corruption
```

장시간 training에서는 reliability가 Goodput에 직접 영향을 준다.

---

# 27. GPU Memory OOM / Fragmentation

GPU memory보다 많이 allocate하면 CUDA OOM이 발생한다.

또한 총 free memory가 충분해도 큰 contiguous block이 없으면 allocation이 실패할 수 있다.

```text
Free blocks:
[10GB][2GB][5GB][1GB]

Need:
12GB contiguous
```

이 현상을 memory fragmentation이라고 한다.
PyTorch 같은 framework는 caching allocator로 allocation/free overhead와 fragmentation을 줄인다.

---

# 28. Unified Memory Oversubscription

CUDA Unified Memory는 GPU memory가 부족할 때 page를 CPU RAM으로 migrate할 수 있다.

```text
GPU HBM
   ↕
CPU RAM
```

하지만 CPU RAM은 HBM보다 느리므로 performance penalty가 생긴다.

> **Unified Memory oversubscription은 OOM 회피에는 유용하지만 성능 최적화의 최종 답은 아니다.**

---

# 29. Docker + NVIDIA Container Toolkit

GPU container의 핵심 구조:

```text
Container
├─ PyTorch
├─ CUDA Runtime
└─ CUDA Libraries

Host
├─ NVIDIA Driver
├─ libcuda.so
└─ GPU
```

NVIDIA Container Toolkit이 container 시작 시 host driver library를 연결한다.

중요한 점:

> Docker GPU workload는 일반적인 hypervisor 기반 GPU virtualization이 아니므로 적절히 구성하면 bare-metal에 가까운 GPU performance를 낼 수 있다.

NVIDIA Container Toolkit은 Docker뿐 아니라 containerd, Podman과도 사용할 수 있다.

---

# 30. CUDA Runtime / Driver Compatibility

Container의 CUDA runtime이 요구하는 최소 host driver version을 만족해야 한다.

```text
Container CUDA
       ↓
Host NVIDIA Driver
       ↓
GPU
```

새 CUDA image + 너무 오래된 host driver 조합은 오류를 만들 수 있다.

---

# 31. OverlayFS Overhead

Docker container filesystem은 보통 OverlayFS / Copy-on-Write를 사용한다.

AI workload는 dataset read, model loading, checkpoint writing이 많아 overlay overhead가 문제가 될 수 있다.

대규모 데이터는 image 안에 넣기보다 host filesystem을 bind mount하는 것이 좋다.

```text
Host NVMe / NFS
      ↓
Bind Mount
      ↓
Container
```

장점:

- OverlayFS 우회
- host filesystem 성능 활용
- container image size 감소

---

# 32. Container Image Size

큰 image는 다음을 증가시킨다.

```text
Pull Time ↑
Startup Time ↑
Deployment Time ↑
```

따라서 multi-stage build, 불필요 package 제거, dataset을 image에 포함하지 않는 방법 등을 활용한다.

---

# 33. Kubernetes GPU Scheduling

기본 scheduler가 GPU topology를 무시하면 느린 배치가 생길 수 있다.

예:

```text
GPU 0~3 → 같은 NVLink domain
GPU 4~7 → 다른 NVLink domain
```

4 GPU 요청에 `0,1,4,5`가 배정되면 cross-domain communication이 발생할 수 있다.

이상적 배치:

```text
4 GPUs 요청
 ↓
GPU 0~3
 ↓
같은 NUMA / NVLink domain
```

---

# 34. Kubernetes Topology Manager

Topology Manager는 다음 locality를 고려하도록 도와준다.

- CPU
- NUMA node
- GPU
- PCIe
- NVLink

대표 policy:

```text
best-effort
restricted
single-numa-node
```

NVIDIA GPU Operator / device plugin과 함께 topology-aware scheduling을 구성하는 것이 중요하다.

---

# 35. NVL72에서 Topology

NVL72는 매우 큰 intra-rack NVLink bandwidth를 제공한다.

```text
~1.8 TB/s per GPU
~130 TB/s aggregate
```

따라서 multi-GPU workload는 가능한 한 빠른 NVLink domain 안에 유지하는 것이 유리하다.

```text
Fast:
GPU → NVLink → GPU

Slower:
GPU → NIC → Network → Other Node → GPU
```

---

# 36. Kubernetes vs SLURM

책에서 설명하는 일반적인 경향:

```text
Training Cluster → SLURM
Inference / Service → Kubernetes
```

hybrid solution도 사용할 수 있다.

---

# 37. Kubernetes에서 MIG Scheduling

MIG instance도 Kubernetes resource로 노출할 수 있다.

```yaml
resources:
  limits:
    nvidia.com/mig-2g.45gb: "2"
```

중요:

> Pod는 여러 node에 걸쳐 배치될 수 없으므로 요청한 MIG slice들이 하나의 node에 모두 있어야 한다.

---

# 38. Host Networking / RDMA

Kubernetes overlay network는 NAT나 overlay overhead를 만들 수 있다.
performance-sensitive distributed GPU workload에서는 host networking을 고려한다.

```yaml
hostNetwork: true
```

Docker:

```bash
--network=host
```

InfiniBand / RoCE 환경에서는 RDMA device plugin과 GPUDirect RDMA를 활용할 수 있다.

```text
GPU
 ↓
GPUDirect RDMA
 ↓
NIC
 ↓
InfiniBand / RoCE
 ↓
Remote GPU
```

---

# 39. Kubernetes Orchestration Jitter

같은 node에서 여러 workload가 실행되면 다음이 경쟁할 수 있다.

- CPU
- disk I/O
- network
- IRQ
- background daemon

이로 인해 실행 시간과 throughput의 변동, 즉 jitter가 생긴다.

특히 training과 inference를 한 node에 섞으면 debugging과 tuning이 더 어려워질 수 있다.

---

# 40. Resource Requests / Limits

Kubernetes에서는 CPU와 memory를 명시적으로 예약할 수 있다.

```yaml
resources:
  requests:
    cpu: "16"
    memory: "64Gi"
```

CPU Manager를 활용하면 exclusive CPU core allocation도 가능하다.

Guaranteed QoS를 얻으려면 모든 container에 대해 CPU와 memory의:

```text
requests == limits
```

가 되어야 한다.

---

# 41. OOM Killer

Container가 host memory를 과도하게 사용하면 Linux OOM Killer가 process를 종료할 수 있다.

따라서:

- 충분한 memory headroom
- monitoring
- realistic requests / limits

가 필요하다.

장시간 training job이 중간에 죽으면 그동안 사용한 GPU time이 모두 wasted work가 되므로 reliability 역시 Goodput 문제다.

---

# 42. Kubernetes I/O Isolation

CPU / memory는 Kubernetes가 cgroup 기반으로 제어하지만 I/O isolation은 상대적으로 제한적이다.

필요하다면 host에서:

```text
cgroup v2 I/O controller
```

같은 추가 설정이 필요할 수 있다.

즉 GPU node tuning은 Kubernetes YAML만으로 끝나지 않는다.

---

# 43. Host 설정이 Container보다 먼저다

Container는 host kernel을 공유한다.

따라서 다음 설정은 host가 결정한다.

- Hugepages
- CPU governor
- NUMA
- IRQ affinity
- sysctl
- swap
- GPU driver

```text
Host OS tuning
      ↓
Container performance
```

---

# 44. Chapter 3 전체 Performance Chain

```text
Storage
   ↓
CPU Memory
   ↓
CPU Preprocessing
   ↓
Pinned Memory
   ↓
GPU
   ↓
GPU Memory
   ↓
GPU Compute
   ↓
GPU-to-GPU Network
```

어느 한 단계라도 느리면 GPU는 기다린다.

---

# 45. 핵심 최적화 원칙

## ① Locality

CPU, RAM, GPU, NIC를 가능한 같은 NUMA domain에 둔다.

## ② Pinning

```text
CPU Pinning
Memory Binding
Pinned Host Memory
```

를 이용해 불필요한 이동을 줄인다.

## ③ GPU를 계속 먹인다

```text
Prefetch
DataLoader workers
Pinned memory
Async transfer
```

를 사용한다.

## ④ GPU Sharing 전략을 맞춘다

```text
MPS → concurrent sharing
MIG → hardware isolation
```

## ⑤ Container도 topology를 존중해야 한다

Kubernetes scheduler가 hardware topology를 무시하면 bare-metal tuning 효과가 사라질 수 있다.

## ⑥ 빠른 network path를 유지한다

NVLink, RDMA, GPUDirect, Host Networking 등을 활용한다.

## ⑦ Reliability도 Performance다

ECC, OOM prevention, resource isolation, persistence는 장시간 workload의 Goodput을 보호한다.

---

# 46. 핵심 암기

```text
NUMA
= CPU / RAM / GPU locality가 중요
```

```text
CPU Pinning
= GPU feeding thread를 local CPU에 고정
```

```text
Memory Binding
= local NUMA RAM 사용
```

```text
Pinned Memory
= page-locked host RAM
= faster DMA / H2D copy
```

```text
THP
= training throughput에는 유리할 수 있음
= low-latency inference에는 pause 위험
```

```text
Persistence Mode
= GPU cold-start overhead 감소
```

```text
MPS
= 여러 process의 GPU kernel을 concurrent하게 실행
```

```text
MIG
= 하나의 GPU를 hardware partition
```

```text
ECC
= serious AI workload에서는 유지 권장
```

```text
Unified Memory Oversubscription
= OOM 회피에는 도움
= CPU memory migration 때문에 느릴 수 있음
```

```text
NVIDIA Container Toolkit
= Container CUDA Runtime + Host GPU Driver 연결
```

```text
Topology Manager
= CPU / NUMA / GPU topology-aware scheduling
```

```text
Host Networking / RDMA
= Distributed GPU network overhead 감소
```

```text
Goodput
= 전체 stack에서 실제 유용한 work를 최대화
```

---

# 한 줄 요약

> **Chapter 3의 핵심은 GPU 자체를 튜닝하는 것이 아니라, CPU·NUMA·메모리·OS·드라이버·Docker·Kubernetes까지 전체 실행 환경을 topology-aware하게 구성해 GPU가 기다리는 시간을 최소화하는 것이다.**
