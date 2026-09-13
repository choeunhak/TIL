# Grace–Blackwell Hardware 정리
> Source: *AI Systems Performance Engineering* — Chris Fregly  
> 범위: Chapter 1–2

---

# 1. Grace Blackwell이 중요한 이유

현대 AI 시스템은 단순히 GPU 한 장의 성능만 높인다고 해결되지 않는다.

대규모 LLM에서는 다음 요소가 모두 병목이 될 수 있다.

- GPU 연산 성능
- GPU 메모리 용량 / 대역폭
- CPU ↔ GPU 데이터 이동
- GPU ↔ GPU 통신
- 노드 간 네트워크
- 전력
- 냉각

NVIDIA Grace Blackwell은 이런 문제를 개별 부품 수준이 아니라
**하나의 AI 시스템 전체 관점에서 co-design**한 아키텍처다.

핵심 개념은 다음과 같다.

> CPU + GPU + Memory + Network를 하나의 거대한 AI 컴퓨팅 시스템처럼 동작하게 만든다.

이러한 설계 철학을 책에서는 **Mechanical Sympathy**라고 설명한다.

즉,

> 소프트웨어와 알고리즘이 하드웨어 구조를 이해하고 최대한 활용하도록 함께 설계한다.

---

# 2. Grace Blackwell Superchip

Grace Blackwell Superchip(GB200)은 다음으로 구성된다.

```text
1 × NVIDIA Grace CPU
        +
2 × NVIDIA Blackwell GPU
```

즉 하나의 Superchip에

- Grace CPU 1개
- Blackwell GPU 2개

가 포함된다.

```text
        Blackwell GPU
              │
              │
Grace CPU ─ NVLink-C2C
              │
              │
        Blackwell GPU
```

CPU와 GPU 사이에는 PCIe 대신 **NVLink-C2C**가 사용된다.

---

# 3. 기존 CPU-GPU 구조의 문제

일반적인 GPU 서버는 다음 구조를 가진다.

```text
CPU Memory
    │
   PCIe
    │
GPU Memory
```

CPU와 GPU의 메모리가 분리되어 있기 때문에
데이터를 GPU에서 사용하려면 보통 복사가 필요하다.

예:

```text
CPU RAM
   ↓
PCIe
   ↓
GPU HBM
```

이 과정은 AI workload에서 상당한 병목이 될 수 있다.

특히

- embedding
- KV cache
- 대형 parameter
- training dataset

처럼 이동해야 할 데이터가 많을수록 문제가 커진다.

---

# 4. NVLink-C2C

Grace Blackwell은 CPU와 GPU를 **NVLink-C2C (Chip-to-Chip)** 로 연결한다.

대역폭은 최대 약

```text
~900 GB/s
```

수준이다.

비교하면:

| Interconnect | 대략적인 대역폭 |
|---|---:|
| PCIe Gen5 x16 | ~64 GB/s / direction |
| PCIe Gen6 x16 | ~128 GB/s / direction |
| NVLink-C2C | ~900 GB/s |

즉 CPU-GPU 간 통신이 PCIe보다 훨씬 빠르다.

또 하나의 중요한 특징은

```text
Cache Coherent
```

하다는 점이다.

CPU와 GPU가 메모리의 동일한 값을 일관되게 볼 수 있다.

---

# 5. Unified CPU-GPU Memory

Grace Blackwell에서는 CPU와 GPU 메모리를 하나의
**coherent address space**로 사용할 수 있다.

NVIDIA는 이를 다음과 같이 부른다.

```text
Unified CPU-GPU Memory
또는
Extended GPU Memory (EGM)
```

개념적으로는 다음과 같다.

```text
       Unified Address Space

┌───────────────────────────┐
│ Grace CPU LPDDR5X         │
│                           │
│ Blackwell GPU HBM         │
│                           │
│ Blackwell GPU HBM         │
└───────────────────────────┘
```

GPU가 CPU memory를 직접 접근할 수 있고,
CPU 역시 GPU memory에 접근할 수 있다.

---

# 6. 하지만 CPU Memory와 GPU HBM은 성능이 다르다

Unified Memory라고 해서 성능까지 동일한 것은 아니다.

GPU의 HBM이 훨씬 빠르다.

따라서 이상적인 구조는 다음과 같다.

```text
HOT DATA
   ↓
GPU HBM

COLD / OVERFLOW DATA
   ↓
CPU LPDDR5X
```

즉

- 자주 쓰는 데이터 → HBM
- 덜 자주 쓰는 데이터 → CPU memory

에 두는 것이 좋다.

CPU memory는 GPU 입장에서는

> 매우 크지만 조금 느린 확장 GPU memory

처럼 사용할 수 있다.

---

# 7. Grace CPU

Grace CPU는 NVIDIA가 설계한 ARM 기반 CPU이다.

Architecture:

```text
ARM Neoverse V2
```

Grace CPU의 역할은 GPU가 잘하지 못하는 작업을 처리하는 것이다.

대표적인 작업:

- 데이터 preprocessing
- tokenization
- augmentation
- storage I/O 관리
- GPU kernel launch
- control-heavy workload
- random memory access

즉 Grace CPU는

```text
GPU Feeding Engine
```

역할을 한다.

GPU가 데이터 부족 때문에 놀지 않도록 빠르게 데이터를 공급하는 것이 핵심이다.

메모리는 LPDDR5X 기반이며
메모리 대역폭은 약

```text
~500 GB/s
```

수준이다.

---

# 8. Blackwell GPU

Blackwell의 가장 중요한 특징 중 하나는

```text
Dual-Die GPU
```

라는 점이다.

기존 GPU는 하나의 거대한 GPU die를 사용했지만,
Blackwell은 두 개의 GPU die를 하나의 GPU처럼 사용한다.

```text
Blackwell GPU

┌─────────────┐
│ GPU Die #1  │
└──────┬──────┘
       │
     NV-HBI
       │
┌──────┴──────┐
│ GPU Die #2  │
└─────────────┘
```

두 die는

```text
NV-HBI
(NVIDIA High Bandwidth Interface)
```

로 연결된다.

대역폭은 약

```text
10 TB/s
```

이다.

소프트웨어 입장에서는 두 die가 아니라

```text
하나의 GPU
```

처럼 보인다.

---

# 9. Blackwell B200 vs Hopper H100

책에서 비교하는 주요 차이:

| 항목 | Hopper H100 | Blackwell B200 |
|---|---:|---:|
| Transistors | ~80B | ~208B |
| GPU 구조 | Single Die | Dual Die |
| GPU Memory | ~80 GB | 192 GB (약 180 GB usable) |
| Memory | HBM3 | HBM3e |
| Memory Bandwidth | ~3.35 TB/s | ~8 TB/s |
| L2 Cache | ~50 MB | ~126 MB |

Blackwell은 Hopper보다

- 메모리 용량 증가
- 메모리 대역폭 증가
- cache 증가
- compute 증가

가 동시에 이루어졌다.

---

# 10. HBM3e

Blackwell B200은 GPU당

```text
192 GB HBM3e
```

를 탑재한다.

다만 실제 usable memory는 약

```text
180 GB
```

수준이다.

이유는

- ECC
- system firmware
- manufacturing reservation

등 때문이다.

Blackwell의 HBM bandwidth는 약

```text
8 TB/s
```

로 매우 높다.

---

# 11. GPU Memory Hierarchy

GPU memory는 여러 단계로 구성된다.

```text
Registers
   ↓
Shared Memory / L1
   ↓
L2 Cache
   ↓
HBM
```

성능은 위쪽일수록 빠르다.

따라서 GPU 최적화의 중요한 원칙은

> 데이터를 가능한 한 상위 memory hierarchy에 오래 유지한다.

Blackwell의 126 MB L2 cache는
이 데이터 재사용을 크게 돕는다.

---

# 12. Streaming Multiprocessor (SM)

GPU는 많은 수의

```text
Streaming Multiprocessor (SM)
```

로 구성된다.

각 SM에는 다음이 포함된다.

- FP32 unit
- INT32 unit
- Tensor Core
- Load / Store unit
- Special Function Unit
- Registers
- Shared Memory
- L1 Cache

CPU core와 비슷한 역할을 하지만,
GPU의 SM은 대규모 병렬처리에 특화되어 있다.

---

# 13. Thread와 Warp

CUDA에서는 thread를

```text
Warp
```

단위로 실행한다.

하나의 warp는

```text
32 threads
```

이다.

32개의 thread가 동일한 instruction을 수행하는 방식을

```text
SIMT
Single Instruction Multiple Threads
```

라고 한다.

---

# 14. Latency Hiding

어떤 Warp가 memory access를 기다리는 동안 다른 warp를 실행한다.

```text
Warp A → memory 기다림
Warp B → 실행
Warp C → 실행
Warp D → 실행
```

이를

```text
Latency Hiding
```

이라고 한다.

GPU에 충분히 많은 warp가 올라가 있으면 memory latency를 숨길 수 있다.

---

# 15. Tensor Core

Tensor Core는 GPU 내부의 AI 전용 matrix 연산 장치다.

Transformer workload의 핵심 계산은 대부분 matrix multiplication이다.

---

# 16. Transformer Engine

NVIDIA는 Transformer workload 최적화를 위해

```text
Transformer Engine (TE)
```

을 제공한다.

핵심은 Mixed Precision이다.

```text
FP16
 ↓
FP8
 ↓
FP4
```

precision을 낮추면

1. 연산량 증가
2. memory 사용 감소
3. memory bandwidth 요구량 감소

효과가 발생한다.

---

# 17. FP16 → FP8 → FP4

책에서는 대략적인 상대 성능을 다음과 같이 설명한다.

```text
FP16 : 1×
FP8  : 2×
FP4  : 4×
```

Memory usage 역시 감소한다.

```text
FP16 = 16 bits
FP8  = 8 bits
FP4  = 4 bits
```

---

# 18. Grace Blackwell NVL72

대표적인 시스템이

```text
GB200 NVL72
```

이다.

구성:

```text
36 Grace CPUs
72 Blackwell GPUs
```

즉 36개의 Grace Blackwell Superchip이 들어간다.

---

# 19. NVL72 Compute Tray

NVL72는 총

```text
18 compute trays
```

로 구성된다.

각 compute tray:

```text
2 × Grace Blackwell Superchip
= 2 Grace CPU
+ 4 Blackwell GPU
```

따라서:

```text
18 trays × 4 GPUs = 72 GPUs
```

---

# 20. NVLink 5

GPU 간 연결에는

```text
NVLink 5
```

가 사용된다.

Blackwell GPU당 NVLink bandwidth:

```text
1.8 TB/s
```

GPU 하나당 NVLink 5 link:

```text
18개
```

이다.

---

# 21. NVSwitch

72개의 GPU를 연결하기 위해

```text
NVSwitch
```

가 사용된다.

NVSwitch는 쉽게 말해

```text
GPU 전용 초고속 Network Switch
```

이다.

NVL72에는 총

```text
18 NVSwitch chips
```

가 사용된다.

---

# 22. NVL72 Network Topology

NVL72는 GPU 사이를 거의

```text
Full Crossbar
```

처럼 연결한다.

즉:

```text
GPU A → NVSwitch → GPU B
```

의 단일 switch hop으로 통신할 수 있다.

전체 GPU interconnect bandwidth는 약

```text
130 TB/s
```

수준이다.

---

# 23. 기존 GPU Cluster와 NVL72 비교

기존 GPU cluster:

```text
GPU
 ↓
PCIe
 ↓
CPU
 ↓
NIC
 ↓
InfiniBand / Ethernet
 ↓
NIC
 ↓
CPU
 ↓
GPU
```

NVL72:

```text
GPU
 ↓
NVLink
 ↓
NVSwitch
 ↓
GPU
```

따라서

- latency 감소
- bandwidth 증가
- CPU intervention 감소

가 가능하다.

---

# 24. Multi-GPU Programming

NVL72에서는 GPU가 다른 GPU의 memory에 접근할 수 있다.

대표적인 기술:

```text
NCCL
NVSHMEM
GPUDirect RDMA
```

특히 NVSHMEM은 GPU 간 one-sided memory access를 지원한다.

---

# 25. GPUDirect RDMA

노드가 달라지면 NVLink만으로는 부족하다.

이때 사용되는 기술이

```text
GPUDirect RDMA
```

이다.

일반적인 network transfer:

```text
GPU
 ↓
CPU RAM
 ↓
NIC
 ↓
Network
```

GPUDirect RDMA:

```text
GPU
 ↓
NIC
 ↓
Network
```

CPU RAM을 거치지 않는다.

---

# 26. SHARP

NVIDIA는 network switch 자체에서 일부 collective 연산을 수행한다.

이를

```text
SHARP
Scalable Hierarchical Aggregation and Reduction Protocol
```

이라고 한다.

즉 In-Network Computing이다.

장점:

- GPU 부담 감소
- network traffic 감소
- collective latency 감소

---

# 27. NVL72 Rack Memory

GB200 NVL72 전체 GPU HBM은 약

```text
72 × 192 GB ≈ 13.8 TB
```

이다.

Grace CPU memory까지 포함하면 약

```text
30 TB
```

규모의 memory를 하나의 NVLink domain에서 사용할 수 있다.

---

# 28. NVL72 Compute Performance

GB200 NVL72의 이론적인 성능은

FP4 기준:

```text
≈ 1.44 ExaFLOPS
```

FP8 기준:

```text
≈ 720 PetaFLOPS
```

이다.

그래서 NVIDIA는 NVL72를

```text
AI Supercomputer in a Rack
```

이라고 부른다.

---

# 29. NVL72 Power

NVL72 rack은 최대 약

```text
120~130 kW
```

를 소비한다.

대략:

```text
18 Compute Nodes ≈ 110 kW
NVSwitch + Cooling + 기타 ≈ 20 kW
```

---

# 30. Liquid Cooling

NVL72는 공랭으로 냉각하기 어렵다.

따라서

```text
Liquid Cooling
```

이 필수적으로 사용된다.

구조:

```text
GPU / CPU
   ↓
Cold Plate
   ↓
Coolant
   ↓
CDU
   ↓
Data Center Water Loop
```

CDU:

```text
Coolant Distribution Unit
```

---

# 31. NVL72가 무거운 이유

NVL72는

```text
약 3,000 lb
≈ 1.3~1.4 ton
```

수준의 무게를 가진다.

따라서 AI infrastructure는

```text
전력
냉각
바닥 하중
랙 설계
```

까지 고려해야 한다.

---

# 32. Monitoring

NVIDIA에서는

```text
DCGM
Data Center GPU Manager
```

를 통해 다음을 모니터링할 수 있다.

- GPU utilization
- GPU memory
- temperature
- power
- NVLink traffic
- ECC errors

---

# 33. Goodput

Goodput은

> 실제로 유용한 AI 계산을 수행한 throughput

이다.

예:

```text
Theoretical throughput
12,000 tokens/s

Actual throughput
10,000 tokens/s

Goodput
= 10,000 / 12,000
= 83.3%
```

AI Performance Engineering의 목표는

```text
Goodput → 100%
```

에 가깝게 만드는 것이다.

---

# 34. Hardware-Software Co-design

Grace Blackwell의 핵심 철학은

```text
Hardware
   ↕
Software
   ↕
Algorithm
```

을 함께 설계하는 것이다.

Transformer가 등장하면서 중요해진

```text
Matrix Multiplication
Attention
Softmax
```

에 맞춰 NVIDIA는

- Tensor Core
- Transformer Engine
- FP8
- FP4
- Special Function Unit
- NVLink

등을 발전시켰다.

반대로 새로운 hardware capability가 생기면서

- FlashAttention
- MLA
- Quantization
- MoE

같은 알고리즘이 발전했다.

---

# 35. 전체 구조 정리

Grace Blackwell NVL72를 계층적으로 보면:

```text
AI Application
      │
      ▼
PyTorch / vLLM
      │
      ▼
CUDA / NCCL
      │
      ▼
Tensor Core / SM
      │
      ▼
Blackwell GPU
      │
      ▼
NVLink
      │
      ▼
NVSwitch
      │
      ▼
72 GPU NVLink Domain
      │
      ▼
InfiniBand / Ethernet
      │
      ▼
Multi-Rack AI Factory
```

CPU 측에서는:

```text
Grace CPU
   │
NVLink-C2C
   │
Blackwell GPU
```

이 구조로 연결된다.

---

# 36. Grace Blackwell을 이해할 때 핵심 포인트

## ① GPU만 빠른 시스템이 아니다

Grace Blackwell의 핵심은 GPU 자체 성능보다

```text
CPU
Memory
GPU
Network
Cooling
Power
```

를 하나의 시스템으로 최적화했다는 점이다.

## ② Memory가 매우 중요하다

Blackwell은

- HBM3e
- 8 TB/s bandwidth
- 126 MB L2
- Unified CPU-GPU memory

를 제공한다.

## ③ Communication이 성능을 결정한다

GPU가 많아질수록 GPU ↔ GPU Communication이 중요해진다.

따라서 NVIDIA는

```text
NVLink
NVSwitch
NCCL
SHARP
GPUDirect RDMA
```

를 통해 communication bottleneck을 줄인다.

## ④ Precision은 핵심 performance lever

```text
FP16
 ↓
FP8
 ↓
FP4
```

로 precision을 낮추면

```text
Compute ↑
Memory usage ↓
Memory bandwidth requirement ↓
```

효과가 있다.

## ⑤ 결국 목표는 Goodput

최종 목표는

```text
Useful AI Work / Time
```

을 최대화하는 것이다.

---

# 핵심 암기

```text
Grace Blackwell Superchip
= 1 Grace CPU + 2 Blackwell GPUs
```

```text
Blackwell
= Dual-Die GPU
```

```text
CPU ↔ GPU
= NVLink-C2C (~900 GB/s)
```

```text
Blackwell GPU HBM
= 192 GB / 약 180 GB usable
```

```text
HBM Bandwidth
= ~8 TB/s
```

```text
Blackwell L2
= ~126 MB
```

```text
NVL72
= 36 Grace CPU + 72 Blackwell GPU
```

```text
GPU NVLink
= ~1.8 TB/s per GPU
```

```text
NVL72 NVLink Fabric
= ~130 TB/s
```

```text
NVL72 Compute
= ~1.44 ExaFLOPS FP4
```

```text
NVL72 Power
= ~130 kW
```

```text
핵심 철학
= Mechanical Sympathy
= Hardware + Software + Algorithm Co-design
```

---

# 한 줄 요약

> **Grace Blackwell은 CPU–GPU–메모리–네트워크를 하나의 거대한 AI 컴퓨터처럼 결합한 아키텍처이며, NVLink·Unified Memory·Tensor Core·FP4·NVSwitch를 통해 초대형 LLM의 계산과 통신 병목을 동시에 줄이는 것이 핵심이다.**
