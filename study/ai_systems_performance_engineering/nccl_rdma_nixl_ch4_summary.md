# NCCL, RDMA, NIXL 정리

> Source: *AI Systems Performance Engineering* - Chris Fregly
> 범위: Chapter 4 - Tuning Distributed Networking Communication

---

## 1. 이 장의 문제: GPU가 다른 GPU를 기다린다

대규모 학습과 추론에서는 GPU 연산만 빠르다고 전체 시스템이 빨라지지 않는다. GPU 간 gradient 동기화, 노드 간 tensor 이동, 스토리지에서의 데이터 로드, 추론 단계 사이의 KV cache 이동이 병목이 될 수 있다.

이 장의 목표는 다음 세 가지다.

1. 통신을 연산과 겹쳐 GPU 유휴 시간을 숨긴다.
2. 가장 빠른 하드웨어 경로(NVLink, NVSwitch, InfiniBand/RoCE RDMA)를 실제로 사용한다.
3. 학습의 집단 통신에는 NCCL, 분리형 추론의 비동기 전송에는 NIXL을 사용한다.

핵심은 **통신을 없애는 것이 아니라, 전송량·횟수·대기 시간을 줄이고 남은 통신을 연산 뒤에 숨기는 것**이다.

```text
통신을 기다리는 구조
연산 ──────────── 통신 ──────────── 다음 연산

통신을 겹치는 구조
연산 ──────────── 다음 연산
      통신 ────────────
```

---

## 2. 통신과 연산의 오버랩

### CUDA stream과 비동기 실행

CUDA stream은 GPU 작업 큐다. 연산용 stream과 통신용 stream을 분리하면, 서로 의존하지 않는 작업은 동시에 진행될 수 있다.

```text
compute stream:  matrix multiply ───── next layer backward
comm stream:                  all-reduce ─────────────
```

PyTorch DDP는 backward 중 gradient가 준비되는 즉시 bucket 단위로 NCCL all-reduce를 통신 stream에 제출한다. 이후 레이어의 gradient 계산은 기본 stream에서 계속한다. backward가 모두 끝난 뒤에 all-reduce를 한 번에 실행하는 방식보다 iteration 시간이 짧아진다.

다만 오버랩은 자동으로 항상 최대가 되지 않는다.

- 모델이 작아 gradient가 하나의 bucket에 들어가면 통신 시작이 늦다.
- 마지막 gradient bucket은 뒤에 남은 연산이 없어 통신 시간이 드러나는 tail이 된다.
- `torch.cuda.synchronize()`는 모든 GPU 작업을 기다리게 한다.
- `tensor.item()`처럼 GPU tensor를 CPU 값으로 가져오는 작업도 동기화를 유발할 수 있다.

동기화는 정확한 측정 또는 의존성 처리 시점에만 사용하고, iteration 중간에는 불필요하게 넣지 않는다.

### 통신 횟수와 전송량 줄이기

오버랩과 함께 다음 방법을 사용한다.

- **Gradient accumulation**: 여러 minibatch의 gradient를 누적한 뒤 한 번 동기화한다. 통신 횟수는 줄지만 effective batch size와 메모리 사용량은 늘어난다.
- **Compression / quantization / sparsification**: 보내는 gradient 양을 줄인다. 정확도와 알고리즘 복잡도의 비용이 있다.
- **Bucketing**: 작은 tensor를 묶어 호출 오버헤드를 줄이고, 준비된 bucket부터 일찍 전송한다.

DDP의 bucket이 너무 크면 대역폭은 잘 쓰지만 시작이 늦고, 너무 작으면 NCCL 호출이 많아진다. 기본값을 출발점으로 삼고 PyTorch Profiler나 Nsight Systems에서 실제 iteration time을 비교한다.

---

## 3. Magnum IO와 데이터 경로

Magnum IO는 GPU, NIC, 스토리지 사이의 데이터 이동을 가속하는 NVIDIA 기술 묶음이다.

- **NCCL**: 여러 GPU의 collective communication
- **GPUDirect RDMA**: NIC와 GPU HBM 사이의 직접 전송
- **GPUDirect Storage(GDS)**: 스토리지와 GPU 메모리 사이의 직접 경로
- **NVLink / NVSwitch**: 노드 또는 NVLink domain 안의 고대역폭 GPU 통신
- **SHARP / NVLS**: 스위치 또는 NVSwitch 내부의 collective 오프로드

좋은 경로는 다음과 같다.

```text
GPU HBM ─ NVLink/NVSwitch ─ GPU HBM             (같은 고속 도메인)
GPU HBM ─ RDMA NIC ─ InfiniBand/RoCE ─ RDMA NIC ─ GPU HBM  (노드 간)
```

나쁜 경로는 GPU 데이터를 CPU RAM에 staging하고, 커널 TCP/IP stack을 지나 보내는 경우다. 이 경로는 CPU 복사·context switch·추가 버퍼 때문에 지연과 CPU 사용량이 커진다.

---

## 4. RDMA와 GPUDirect RDMA

### RDMA

RDMA(Remote Direct Memory Access)는 NIC가 원격 메모리를 직접 읽고 쓰게 하는 기술이다. 일반 TCP 통신처럼 CPU가 패킷마다 복사와 커널 처리를 많이 하지 않아도 된다.

```text
일반 TCP
GPU → CPU RAM → kernel network stack → NIC → network → NIC → CPU RAM → GPU

GPUDirect RDMA
GPU HBM → RDMA NIC → network → RDMA NIC → GPU HBM
```

GPUDirect RDMA에서는 RDMA NIC가 GPU buffer를 등록한 뒤 GPU HBM으로 직접 DMA를 수행한다. CPU는 초기 설정과 completion 처리에는 관여하지만, 데이터 복사 경로의 중심에는 있지 않다.

### InfiniBand와 RoCE

- **InfiniBand**: RDMA를 기본으로 제공하는 고성능 네트워크다.
- **RoCE**: RDMA over Converged Ethernet. RDMA 가능한 Ethernet NIC·스위치와 적절한 네트워크 설정이 필요하다.
- **TCP Ethernet**: RDMA가 없을 때의 대안이다. 대역폭, 버퍼, 혼잡 제어를 조정할 수 있지만 GPUDirect RDMA 경로와 동일하지는 않다.

Ethernet에서 RoCE를 쓴다고 해서 자동으로 좋은 성능이 나는 것은 아니다. MTU, 혼잡 제어, PFC/ECN 같은 패브릭 정책과 NIC·드라이버 구성이 맞아야 한다.

### 실제로 RDMA가 사용되는지 확인

NCCL은 RDMA 사용이 불가능하면 TCP socket으로 조용히 fallback할 수 있다. 학습은 계속되지만 처리량이 크게 떨어질 수 있다.

확인 항목:

```bash
nvidia-smi topo -m
lsmod | grep nvidia_peermem
NCCL_DEBUG=INFO
ibstat
ip -s link show <interface>
```

- 컨테이너에는 `/dev/infiniband` 등 RDMA 장치가 노출되어야 한다.
- 컨테이너의 GID와 host 구성이 맞지 않으면 GPU-direct 등록이 실패할 수 있다.
- RDMA perftest의 CUDA 옵션과 NCCL log로 실제 GPU-direct 경로를 검증한다.
- CPU 사용량이 높고 GPU 통신 대역폭이 낮으면 CPU staging 또는 TCP fallback을 의심한다.

### RDMA도 topology를 탄다

NIC의 IRQ·polling thread와 GPU process는 가능하면 같은 NUMA node의 CPU에 배치한다. RDMA가 직접 전송을 하더라도 제어 경로와 completion 처리는 남아 있기 때문이다.

여러 NIC가 있다면 NCCL이 여러 rail에 traffic을 분산하는 multirail 구성을 사용할 수 있다. 단, NIC가 실제로 다른 PCIe/NUMA 경로에 어떻게 붙었는지 확인하고, thread·socket 수는 조금씩 바꾸며 측정한다.

---

## 5. 멀티노드 통신에서 자주 생기는 문제

### Gloo를 GPU 통신에 사용

NVIDIA GPU 다중 노드 학습의 기본 backend는 보통 `nccl`이다.

```python
dist.init_process_group(backend="nccl")
```

`gloo`는 CPU와 TCP 중심 backend다. GPU collective에 적합하지 않으며, host staging 또는 실패로 이어질 수 있다. 코드가 실행된다는 사실만으로 GPU-direct 통신이 정상이라는 뜻은 아니다.

### 잘못된 NIC 또는 느린 management network 선택

여러 interface가 있으면 bootstrap 또는 socket 경로가 느린 관리망으로 잡힐 수 있다. `NCCL_SOCKET_IFNAME`으로 의도한 interface를 지정할 수 있지만, 먼저 로그와 interface counter로 실제 경로를 확인해야 한다.

### 네트워크 대역폭 부족과 port 문제

- GPU 수가 늘수록 all-reduce가 NIC 링크를 포화시킬 수 있다.
- NCCL bootstrap은 TCP port를 사용하므로 대규모 job에서는 ephemeral port 범위도 확인한다.
- TCP 기반 경로라면 socket buffer와 congestion control이 고대역폭 링크를 제한하지 않는지 확인한다.

### Straggler

collective은 모든 rank가 참여해야 한다. 가장 느린 GPU, NIC, 노드 하나가 전체 iteration의 속도를 결정한다.

- 서로 다른 인스턴스 유형·링크 속도·스위치 경로를 섞지 않는다.
- DCGM, NIC counter, temperature, `monitored_barrier`로 느린 rank를 찾는다.
- `NCCL_ASYNC_ERROR_HANDLING=1`과 NCCL log를 사용해 오류와 timeout을 빠르게 드러낸다.

### GPU memory fragmentation과 등록 buffer

PyTorch caching allocator는 해제된 GPU memory를 재사용하려고 reserved 상태로 유지한다. UCX/RDMA의 장기 등록 buffer와 다양한 크기의 tensor 할당이 겹치면 fragmentation 또는 registration pool 압박이 생길 수 있다.

`memory_allocated()`와 `memory_reserved()`를 함께 관측한다. `empty_cache()`는 일시적인 진단 수단일 뿐 근본 해결책은 아니다. allocator 설정, tensor 수명, buffer 재사용 방식을 먼저 점검한다.

---

## 6. NCCL

NCCL(NVIDIA Collective Communications Library)은 여러 NVIDIA GPU가 함께 수행하는 **collective communication** 라이브러리다.

주요 collective:

- **all-reduce**: 모든 rank의 값을 합치거나 평균낸 뒤 모두에게 결과를 전달한다. DDP gradient 동기화의 핵심이다.
- **all-gather**: 각 rank의 조각을 모아 모든 rank가 전체를 갖게 한다.
- **reduce-scatter**: 전체 reduction 결과를 rank별 조각으로 나눠 전달한다.
- **broadcast**: 한 rank의 데이터를 모두에게 보낸다.
- **send / recv**: point-to-point도 가능하지만, NCCL의 주력은 collective이다.

NCCL은 PCIe, NVLink, NVSwitch, InfiniBand, RoCE, TCP socket을 탐지하고 collective별로 가능한 빠른 경로와 알고리즘을 선택한다.

### Topology awareness

같은 8개 GPU라도 연결 구조가 다르면 성능이 다르다.

```text
빠른 경로: 같은 NVLink/NVSwitch domain
중간 경로: 같은 PCIe switch
느린 경로: 다른 NUMA domain, 다른 node, TCP fallback
```

NCCL은 가능한 한 NVLink/NVSwitch 안에서 먼저 reduce하고, 상대적으로 느린 PCIe·node 간 링크에는 줄어든 데이터를 보내는 계층형 방식을 사용한다.

`nvidia-smi topo -m`으로 기본 topology를 보고, 복잡한 NVSwitch 환경은 `nvidia-smi nvlink`, Nsight Systems, `NCCL_TOPO_DUMP_FILE`로 추가 확인한다. 성능이 낮다면 무조건 환경 변수를 바꾸기보다 먼저 job이 느린 연결을 가로질러 배치됐는지 확인한다.

### NCCL 알고리즘

| 알고리즘 | 장점 | 주로 유리한 경우 |
|---|---|---|
| Ring | 링크 부하가 균등하고 대역폭 활용이 좋음 | 큰 message |
| Tree / NVLSTree | 단계 수가 `O(log N)`으로 작음 | 작은 message, latency 지배 상황 |
| CollTree | node 안은 빠른 tree, node 사이는 계층형 tree | 작은·중간 message의 다중 노드 통신 |
| CollNet | local collective와 node 간 tree 결합 | 대규모 다중 노드 |
| PAT | tree 지연 시간과 ring급 처리량을 chunk pipeline으로 결합 | 큰 message에서 높은 처리량과 낮은 지연을 함께 원할 때 |

NCCL은 message 크기, GPU 세대, topology에 따라 자동 선택한다. `NCCL_ALGO` 강제 지정은 profiling으로 자동 선택이 부적절하다는 증거가 있을 때의 실험·진단용이다.

### DP와 DDP

- `nn.DataParallel`은 한 Python process가 여러 GPU를 제어한다. GPU 0에 gather 부담이 모이고 Python GIL과 동기식 gradient 집계 때문에 확장성이 낮다.
- `DistributedDataParallel`은 GPU당 하나의 process를 사용한다. NCCL all-reduce를 backward와 겹치고, 특정 GPU에 집계 부담이 몰리지 않는다.
- FSDP는 parameter·gradient·optimizer state 등을 shard해 메모리 사용량을 줄이는 별도 전략이다.

실제 multi-GPU 학습에서는 보통 DDP 또는 더 큰 모델을 위한 FSDP·tensor/pipeline/expert parallel 조합을 사용한다.

### Communicator lifecycle

NCCL communicator 초기화는 rank 간 handshake, topology 탐색, buffer 설정이 필요해 비싸다.

```text
좋은 구조:  시작 시 init_process_group 1회 → 모든 iteration에서 재사용 → 종료 시 destroy
나쁜 구조:  매 iteration마다 init/destroy
```

모델 병렬용 subgroup도 시작 시 한 번 만들고 재사용한다. dynamic membership과 communicator 생성·종료는 모든 rank가 lockstep으로 호출하지 않으면 hang의 원인이 된다.

### 운영과 진단

- `NCCL_DEBUG=INFO`: topology, NET/IB, fallback 확인용. 운영에서는 과도한 DEBUG logging을 피한다.
- `NCCL_ASYNC_ERROR_HANDLING=1`: network·rank 오류 발생 시 전체 job이 무한 대기하는 위험을 줄인다.
- `NCCL_P2P_DISABLE=1`, `NCCL_SHM_DISABLE=1`: 진단에는 쓸 수 있지만 production에 남기면 intra-node 성능을 크게 떨어뜨린다.
- `NCCL_NSOCKS_PERTHREAD`, `NCCL_SOCKET_NTHREADS`: TCP/socket 기반 또는 multirail 상황에서만 단계적으로 측정하며 조정한다.
- `NCCL_MIN_NCHANNELS`, `NCCL_MAX_NCHANNELS`: GPU 자원도 사용하므로 기본 자동 tuning을 우선한다.
- CPU affinity를 너무 좁게 주면 NCCL polling·dispatch thread가 한 코어에 몰릴 수 있다. GPU와 가까운 NUMA CPU 범위를 충분히 주고 필요 시 `NCCL_IGNORE_CPU_AFFINITY=1`을 검토한다.

---

## 7. SHARP, NVLS, 등록 buffer

**SHARP**는 InfiniBand switch가 reduction 일부를 수행하는 in-network aggregation이다. GPU가 중간 결과를 서로 반복 전송하는 양을 줄인다.

**NVLS(NVLink SHARP)**는 NVSwitch fabric 안에서 유사한 역할을 한다. multicast all-gather와 switch 내 reduce-scatter를 조합해 endpoint의 전송량과 직렬 hop을 줄인다.

SHARP/NVLS는 특히 많은 node·GPU가 참여해 network가 병목인 large all-reduce에서 유리하다. 하지만 지원 switch, firmware, plugin, GPUDirect RDMA 설정이 모두 필요하고, switch buffer 한계 때문에 일부 큰 collective은 일반 경로로 fallback할 수 있다. NCCL log로 실제 사용 여부를 확인한다.

NCCL user buffer registration은 tensor buffer를 직접 collective에 등록해 staging copy와 내부 channel 압박을 줄이는 기능이다. 장기 재사용 buffer에서 효과적일 수 있지만, rank 간 등록 조건과 offset 제약이 있으므로 API 조건을 맞춰야 한다.

---

## 8. NIXL

NIXL(NVIDIA Inference Xfer Library)은 대규모 분산 추론을 위한 비동기 point-to-point 전송 라이브러리다.

NCCL이 여러 GPU가 동시에 맞춰야 하는 all-reduce 같은 many-to-many collective에 강하다면, NIXL은 다음처럼 한 stage에서 다른 stage로 큰 데이터를 보내는 경우에 맞다.

```text
prefill GPU → KV cache → decode GPU
GPU → CPU DRAM
GPU → NVMe / object storage
```

NIXL은 NCCL의 대체재가 아니라 보완재다.

### Disaggregated prefill/decode

LLM 추론은 크게 두 단계로 나뉜다.

- **Prefill**: prompt 전체를 처리하고 KV cache를 만든다. 많은 matrix multiplication을 수행하므로 대체로 compute-bound다.
- **Decode**: KV cache를 사용해 다음 token을 반복 생성한다. model weight와 cache 접근이 많아 대체로 memory-throughput-bound다.

둘을 같은 GPU cluster에서 처리하는 monolithic serving 대신, prefill cluster와 decode cluster를 분리할 수 있다. 이때 prefill 결과인 KV cache를 빠르게 넘겨야 분리의 이점이 생긴다. NIXL은 이 KV cache 이동을 담당한다.

### 경로 선택과 memory tier

NIXL은 source와 destination의 위치를 보고 사용 가능한 backend 중 빠른 경로를 선택한다.

```text
같은 board/node: NVLink, NVLink-C2C, PCIe
같은 NVLink domain: NVSwitch
다른 node/rack: InfiniBand 또는 RoCE GPUDirect RDMA
storage: GDS, NVMe, object-store plugin 등 지원 backend
```

GPU HBM, CPU DRAM, NVMe SSD처럼 서로 다른 memory tier를 하나의 API로 다룬다. 장기 대화나 긴 context의 KV cache가 GPU HBM에 모두 들어가지 않을 때, 덜 자주 쓰는 cache를 CPU memory나 SSD로 offload하고 필요할 때 가져올 수 있다.

### 비동기 API 흐름

NIXL 전송은 source와 destination 각각의 `nixlAgent`가 담당한다.

1. agent를 만들고 backend(예: UCX, GDS)를 설정한다.
2. 전송할 memory를 `registerMem`으로 등록한다.
3. 전송 descriptor를 준비한다.
4. `prepXfer`로 요청을 만들고 `postXfer`로 비동기 제출한다.
5. 전송 중에는 다른 compute를 수행한다.
6. `checkXfer`로 완료 여부를 확인하고 handle과 memory registration을 정리한다.

UCX가 InfiniBand, TCP, shared memory 같은 저수준 transport를 제공하고, GPUDirect RDMA 및 IBGDA를 사용할 수 있는 환경에서는 CPU 개입을 더 줄일 수 있다.

전송 완료 전에는 대상 buffer를 읽으면 안 된다. 따라서 NIXL의 비동기성은 동기화가 필요 없다는 뜻이 아니라, **데이터 의존성이 생기는 지점에서만 완료를 확인한다**는 뜻이다.

---

## 9. NCCL과 NIXL 비교

| 구분 | NCCL | NIXL |
|---|---|---|
| 주 용도 | GPU group collective | stage/component 간 대용량 전송 |
| 통신 패턴 | many-to-many | one-to-one, one-to-few |
| 대표 작업 | all-reduce, all-gather, reduce-scatter | KV cache, model shard, pipeline payload 이동 |
| 주 워크로드 | DDP/FSDP 등 분산 학습 | 분리형 LLM 추론, pipeline형 추론 |
| 동기화 성격 | 참여 rank가 collective 호출에 맞춰야 함 | 비동기 send/receive와 완료 확인 |
| topology | ring/tree 및 NVLink/NVSwitch/IB 경로 선택 | source-destination 간 NVLink, RDMA, GDS 등 경로 선택 |
| framework 통합 | PyTorch DDP 등에서 일반적으로 자동 사용 | NVIDIA Dynamo 등 inference runtime 또는 직접 API 사용 |

---

## 10. 실무 점검 순서

1. **측정**: iteration timeline에서 compute와 NCCL 통신이 겹치는지, GPU가 어디서 idle인지 본다.
2. **경로 확인**: `nvidia-smi topo -m`, NCCL log, NIC counter로 NVLink·RDMA·올바른 NIC 사용을 확인한다.
3. **배치 확인**: 통신이 많은 rank와 NIC interrupt/polling thread가 같은 NUMA 영역에 있는지 확인한다.
4. **fallback 제거**: Gloo, TCP socket, management NIC, host staging, P2P 비활성화 여부를 찾는다.
5. **통신량 조정**: batch, accumulation, bucket size, compression의 trade-off를 profiling으로 비교한다.
6. **NCCL 운영 안정성**: communicator를 재사용하고, version·환경 변수·async error handling을 관리한다.
7. **추론 설계**: prefill/decode를 분리할 경우 KV cache 이동 시간이 이득을 상쇄하지 않는지 NIXL 경로와 오버랩을 측정한다.

## 한 줄 요약

> **학습에서는 NCCL로 collective을 topology-aware하게 실행하고 backward와 겹치며, 노드 간 경로는 RDMA로 CPU staging을 줄인다. 분리형 추론에서는 NIXL로 KV cache 같은 큰 데이터를 GPU·CPU·스토리지 사이에 비동기 전송해 prefill과 decode를 독립적으로 확장한다.**
