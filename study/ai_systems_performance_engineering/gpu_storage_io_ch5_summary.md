# Chapter 5. GPU 기반 스토리지 I/O 최적화

> 출처: Chris Fregly, *AI Systems Performance Engineering*  
> 범위: Chapter 5 — *GPU-Based Storage I/O Optimizations*

## 이 장이 다루는 문제

AI 학습에서 GPU가 충분히 빠르더라도, 다음 배치를 스토리지에서 읽고 전처리해서 GPU 메모리에 넣는 경로가 느리면 GPU는 유휴 상태가 된다. 따라서 성능은 GPU 연산만이 아니라 아래 전체 경로의 처리량과 지연 시간으로 결정된다.

```text
스토리지 → 파일시스템/네트워크 → CPU 데이터 로더·전처리 → H2D 전송 → GPU 연산
```

이 장의 목표는 이 경로에서 복사, 작은 I/O, 대기, 불균형을 줄이고 I/O·전처리·GPU 연산을 겹치는 것이다.

---

## 1. 빠른 스토리지와 데이터 지역성

대규모 학습은 수 TB~PB 규모의 텍스트·이미지·오디오·비디오 데이터를 지속해서 읽는다. 필요한 스토리지 대역폭은 GPU 한 장 기준이 아니라 클러스터 전체의 합으로 계산해야 한다.

```text
필요한 총 읽기 대역폭
= GPU 수 × GPU당 필요한 bytes/s
```

예를 들어 GPU 한 장이 학습 중 200 MB/s를 필요로 하면, 8장은 약 1.6 GB/s가 필요하다. GPU 수가 늘어났는데 스토리지와 데이터 로더가 같은 속도라면 추가 GPU는 데이터를 기다리게 된다.

### 데이터는 가능한 한 GPU 가까이에 둔다

- 가장 가까운 위치: 같은 노드의 로컬 NVMe SSD
- 다음 선택지: 같은 랙에서 짧은 네트워크 경로를 쓰는 NVMe-oF
- 대규모 공유 스토리지: Lustre, GPFS/IBM Storage Scale 같은 병렬 파일시스템
- 원격 객체 스토리지: 학습 전에 로컬 NVMe 또는 캐시 계층으로 스테이징

분산 학습에서는 데이터셋을 노드별로 미리 샤딩하고, 각 노드가 자기 로컬 샤드를 주로 읽게 하는 방식이 효과적이다. 네트워크를 통해 같은 데이터를 여러 노드가 반복해서 읽는 일을 줄일 수 있다. PyTorch `DistributedSampler`는 epoch마다 rank별로 서로 다른 샘플을 받도록 조정하는 데 사용된다.

### 지역성만으로 충분하지 않은 이유

로컬 디스크가 있어도 `DataLoader` worker 수가 부족하거나 CPU 전처리가 느리면 GPU는 기다린다. 반대로 worker를 너무 많이 늘리면 CPU 코어와 디스크 I/O를 서로 경쟁하게 된다. 따라서 worker 수, CPU 사용률, 디스크 처리량을 함께 측정해야 한다.

---

## 2. 순차 읽기와 랜덤 읽기

스토리지는 큰 연속 구간을 읽을 때 작은 랜덤 읽기보다 높은 처리량을 내는 경우가 많다.

### 작은 파일이 많은 데이터셋의 문제

수백만 개의 이미지 파일을 각각 열면 파일 열기, 메타데이터 조회, 작은 읽기 요청이 반복된다. 이때 병목은 전송 대역폭이 아니라 요청당 고정 비용과 랜덤 접근 지연 시간이 된다.

가능하면 많은 샘플을 큰 shard 파일로 묶는다.

- Arrow, TFRecord, Parquet
- WebDataset의 tar shard
- 여러 샘플을 담은 바이너리 또는 데이터베이스 파일
- 객체 스토리지에서도 작은 object를 큰 object로 사전 병합

한 번의 읽기로 여러 샘플을 가져올 수 있고, 순차 접근과 read-ahead의 효과도 커진다.

### 읽기 크기와 비동기 I/O

- 4 KB 같은 작은 요청보다 1 MB 수준의 큰 요청이 요청당 오버헤드를 줄인다.
- `DataLoader`의 버퍼 크기와 prefetch 크기를 실제 데이터 크기에 맞게 조정한다.
- 순차 읽기에서는 OS read-ahead가 도움 되지만, 랜덤 읽기에는 효과가 제한적이다.
- 랜덤 접근이 필요하면 여러 `pread()` 요청을 병렬화하거나 `io_uring`으로 요청을 묶어 제출한다.

`io_uring`은 등록 버퍼와 polling 등을 사용해 system call 오버헤드를 줄이고, 여러 I/O 요청을 동시에 제출해 지연 시간을 숨기는 데 쓸 수 있다.

---

## 3. NVMe와 파일시스템 처리량 튜닝

### Linux 블록 I/O 계층

현대 Linux NVMe는 멀티큐 블록 계층(`blk-mq`)을 사용해 여러 CPU 코어에 I/O를 분산한다. NVMe에서는 보통 기본 설정이 적절하지만 다음은 확인할 가치가 있다.

- I/O scheduler: `/sys/block/<device>/queue/scheduler`
- 빠른 NVMe에서 일반적으로 `none` 또는 `mq-deadline`
- 순차 스트리밍의 경우 read-ahead: `/sys/block/<device>/queue/read_ahead_kb`
- PCIe lane 수와 SSD가 실제로 연결된 인터페이스의 대역폭
- 단일 SSD가 부족하면 RAID 0 스트라이핑으로 여러 SSD의 처리량 결합

XFS는 대규모 동시 I/O를 위한 NVMe 서버에서 흔히 사용된다. `noatime` 마운트 옵션은 매 읽기마다 access time을 갱신하는 비용을 없앤다.

### 페이지 캐시와 메모리 적재

Linux page cache는 최근 읽은 데이터를 RAM에 보관한다. 데이터셋이 RAM보다 훨씬 크면 캐시가 계속 교체되어 이점이 작을 수 있다. 반대로 데이터 전체 또는 상당 부분이 CPU 메모리나 Grace Blackwell의 통합 메모리에 들어가면 시작 시 적재해 디스크 I/O를 크게 줄일 수 있다.

PB급 데이터셋은 모두 올려둘 수 없으므로, 이 경우에는 스트리밍 I/O 자체를 최적화해야 한다.

### PyTorch 데이터 로더의 기본 조정점

```python
DataLoader(
    dataset,
    num_workers=N,
    pin_memory=True,
    persistent_workers=True,
    prefetch_factor=...,  # num_workers > 0일 때 worker당 미리 준비할 batch 수
)

# pinned host memory에서 GPU로 비동기 전송
batch = batch.to(device, non_blocking=True)
```

- `num_workers`: 읽기·decode·전처리를 병렬화한다. 적정값은 실측으로 찾는다.
- `pin_memory=True`: H2D DMA에 쓸 page-locked host memory를 사용한다.
- `non_blocking=True`: pinned memory를 소스로 할 때 H2D 전송을 비동기로 실행할 수 있다.
- `persistent_workers=True`: epoch마다 worker를 다시 만들지 않는다.
- `prefetch_factor`: I/O가 순간적으로 느려질 때 큐가 비는 것을 막지만, 너무 높으면 host memory를 많이 사용한다.

pinned memory를 크게 사용할 때는 `ulimit -l` 또는 컨테이너의 `memlock` 제한도 확인해야 한다.

---

## 4. NVIDIA GPUDirect Storage(GDS)

### 기존 경로와 GDS 경로

일반적인 경로에서는 데이터가 먼저 SSD에서 CPU 메모리로 오고, 이후 CUDA 전송으로 GPU HBM으로 복사된다.

```text
일반 경로: SSD/NAS → CPU 메모리 → GPU HBM
GDS 경로 : SSD/NVMe-oF → GPU HBM
```

GDS는 스토리지 또는 네트워크 스토리지와 GPU 메모리 사이의 DMA 경로를 만들어 host memory bounce buffer를 없앤다. CPU가 I/O를 설정하고 제어하는 역할까지 없어지는 것은 아니다.

- GPUDirect RDMA: 네트워크 ↔ GPU DMA 최적화
- GDS: 스토리지 ↔ GPU DMA 최적화

둘 다 CPU 메모리를 중간 복사 버퍼로 쓰지 않게 하지만, CPU의 orchestration은 계속 필요하다.

### 요구 사항과 API

GDS에는 GPU, NVIDIA driver/CUDA Toolkit, DMA를 지원하는 스토리지·파일시스템 조합이 필요하다. 대표적으로 로컬 NVMe, NVMe-oF, RDMA 기반 NFS, 일부 병렬 파일시스템이 해당한다. 애플리케이션은 `cuFile` API를 사용하며, `cuFileRead` 또는 `cuFileReadAsync`로 GDS 경로를 이용한다.

- 가능하면 `O_DIRECT`를 사용해 page cache를 우회하고 직접 DMA 경로를 사용한다.
- 정렬(alignment)이 맞지 않으면 추가 복사가 생기거나 처리량이 낮아질 수 있다.
- GPU device buffer는 `cuFile`에 등록되고, `nvidia-fs` kernel driver가 스토리지/NIC와 GPU 메모리의 DMA를 조율한다.
- `cuFileReadAsync`/`cuFileWriteAsync`는 CUDA stream과 결합해 I/O와 연산을 겹칠 수 있다.

### 언제 효과가 큰가

CPU가 이미 전송을 충분히 감당한다면 처리량 이득은 작을 수 있다. 반면 많은 `memcpy`로 CPU가 포화됐거나, 작은 batch를 매우 높은 빈도로 공급해야 하는 경우에는 CPU 사용률과 복사 단계를 줄여 효과가 커질 수 있다. GDS의 이득은 I/O 크기, queue depth, NIC, 파일시스템에 따라 다르므로 반드시 같은 조건에서 측정한다.

### `gdsio`로 비교 측정

CUDA GDS 도구의 `gdsio`로 CPU 경로와 GDS 경로를 동일한 파일·I/O 크기·worker 수에서 비교한다.

```bash
# -x 2: CPU-mediated transfer 경로
/usr/local/cuda/gds/tools/gdsio -f /mnt/data/large_file \
  -d 0 -w 4 -s 10G -i 1M -I 0 -x 2

# -x 0: GDS 경로
/usr/local/cuda/gds/tools/gdsio -f /mnt/data/large_file \
  -d 0 -w 4 -s 10G -i 1M -I 0 -x 0
```

처리량뿐 아니라 평균 지연 시간, CPU 사용률, 실제 학습 step time까지 비교해야 한다. microbenchmark가 빨라도 전체 파이프라인이 다른 구간에서 막히면 학습 성능은 달라지지 않을 수 있다.

---

## 5. GPU 상태 checkpoint와 스토리지

`cuda-checkpoint`는 Linux에서 실행 중인 CUDA 프로세스의 GPU 상태를 CPU 프로세스 checkpoint 도구(CRIU 등)와 함께 저장·복원하는 경로다.

1. CUDA driver 진입점을 잠그고 제출된 GPU 작업이 끝날 때까지 기다린다.
2. device memory를 driver가 관리하는 host allocation으로 복사한다.
3. GPU 리소스를 해제하고, CPU 측 checkpoint 도구가 프로세스 상태를 저장한다.
4. 복원 시 GPU를 다시 획득하고, device memory와 CUDA context·stream 등을 되살린다.

이 기능은 장시간 작업의 preemption, migration, fault tolerance에 유용하다. 다만 학습 프레임워크의 `state_dict` 또는 sharded checkpoint를 대체하는 기능은 아니다. 특히 이 checkpoint 경로는 GDS처럼 GPU 메모리에서 스토리지로 직접 DMA하지 않고, suspend 시 GPU 메모리 이미지가 먼저 host memory로 이동한다. 따라서 사용 중인 VRAM 크기와 host link 대역폭이 suspend 시간을 좌우한다.

---

## 6. 분산 파일시스템과 객체 스토리지

### NFS

단일 NFS 서버는 여러 노드가 동시에 읽으면 병목이 되기 쉽다. 소규모 클러스터에는 편하지만 대규모 학습에는 보통 병렬 파일시스템이나 캐시 계층이 더 적합하다.

- 서버 NIC와 디스크가 충분히 빠른지 확인한다.
- 여러 NFS 서버로 데이터셋을 분할할 수 있다.
- `rsize`/`wsize`를 크게 잡아 요청당 오버헤드를 줄인다.
- client mount 옵션과 attribute cache도 실제 일관성 요구 사항 안에서 조정한다.

### 객체 스토리지

S3 같은 object store를 학습 중 매번 직접 읽으면 지연 시간과 요청 수가 문제가 될 수 있다.

- 학습 전 로컬 NVMe로 스테이징한다.
- FSx for Lustre 같은 캐시 계층을 사용한다.
- 큰 range request와 다중 스레드 전송을 사용한다.
- `s5cmd`, 최적화된 SDK 등 병렬 전송 도구를 사용한다.

### 병렬 파일시스템

Lustre, GPFS, Ceph 같은 병렬 파일시스템은 여러 storage target이 동시에 파일 일부를 제공하도록 설계된다. 큰 shard 파일을 여러 target에 stripe하면 읽기 처리량을 합산할 수 있다.

모니터링에서 특정 storage node만 과열되어 있으면 샤딩 또는 stripe 설정이 고르지 않을 가능성이 크다. 데이터 분포와 요청 분포를 함께 확인해야 한다.

---

## 7. 복제와 압축의 트레이드오프

### 노드별 복제

데이터셋을 각 compute node의 로컬 저장소에 복제하면 네트워크 읽기를 없앨 수 있다. 성능은 좋지만 저장 공간과 배포·갱신 비용이 늘어난다.

### 압축 저장과 해제

압축 데이터는 저장소에서 읽어야 할 바이트 수를 줄인다. 대신 CPU 또는 GPU에서 decode/decompression 비용이 생긴다.

- I/O 병목이고 CPU/GPU에 여유가 있으면 유리하다.
- decompression이 새 병목이 되면 이득이 사라진다.
- `nvJPEG`는 이미지 decode를 GPU로 옮길 수 있다.
- 최신 GPU의 decompression engine은 LZ4, Snappy, Deflate 같은 형식의 해제를 가속할 수 있다.

핵심은 "읽을 바이트 감소"와 "해제 비용 증가"의 합이 실제로 줄었는지 end-to-end로 검증하는 것이다.

---

## 8. 데이터 파이프라인 전처리

학습 중 데이터 로더가 하는 일은 단순 파일 읽기가 아니다.

```text
읽기 → parse/deserialization → decode → tokenization/augmentation → batch collate → H2D 전송
```

### Python 병목 줄이기

- worker process를 사용해 Python GIL 영향을 줄인다.
- 샘플 하나씩 Python loop로 tokenization·변환하지 말고 batch/vectorized 연산을 우선한다.
- Rust/C++ 기반 tokenizer와 라이브러리를 활용한다.
- `collate_fn` 등을 이용해 tensor 단위로 묶어서 처리한다.
- 디버그 로그나 비싼 CPU transform이 critical path에 들어가지 않게 한다.

### I/O·전처리·GPU 연산 겹치기

이상적인 상태에서는 GPU가 batch N을 연산하는 동안 CPU worker가 batch N+1을 읽고 전처리해 pinned memory에 준비한다. 이후 별도 CUDA stream에서 N+1의 H2D 복사를 시작하고, 연산 stream은 복사 완료 event를 기다린 뒤 사용한다.

중요한 것은 단순히 `non_blocking=True`를 붙이는 것이 아니라, source가 pinned memory이고 stream 간 의존성이 올바르게 설정되어 실제 overlap이 일어나는지 타임라인으로 확인하는 것이다.

### GPU 전처리: NVIDIA DALI

NVIDIA DALI는 이미지·비디오 decode, crop, resize, normalize 같은 작업을 GPU 또는 최적화된 C++ CPU 코드로 실행한다. CPU가 decode/augmentation으로 포화되고 GPU에 여유가 있는 입력 병목 워크로드에서 유용하다.

하지만 GPU에서 decode한 결과를 다시 CPU로 보내 CPU transform을 수행하면 host-device-host 복사가 늘어 이점이 사라질 수 있다. GPU 친화적인 전처리는 GPU graph 안에 남기거나 CUDA 기반 라이브러리로 묶는 편이 좋다. CPU-only, DALI, 완전 GPU 기반 파이프라인을 같은 조건에서 비교한다.

### 오프라인 데이터 준비: NeMo Curator

NeMo Curator는 대규모 LLM/멀티모달 데이터셋의 정제, tokenization, shuffle, deduplication, 품질 필터링, shard 생성 등을 분산 처리하는 도구다.

학습 전에 데이터를 일정한 형식과 크기의 큰 shard로 준비하면, 학습 중에는 원시 텍스트 처리와 무작위 작은 파일 접근을 줄일 수 있다. 여러 epoch의 runtime shuffle 비용이 크면 서로 다른 순서로 섞은 데이터 복사본을 미리 만드는 선택지도 있지만 저장 공간과 교환한다.

---

## 9. 관측과 병목 분리

### 계층별 도구

- host I/O: `iostat`, `iotop`, `nvme-cli`, `perf`, eBPF
- GPU 및 I/O: DCGM, Nsight Systems
- GDS 타임라인: `nsys --trace=gds`, cuFile tracepoint
- kernel 수준: Nsight Compute

PyTorch에서 `next(data_iterator)` 시간은 Python 로더뿐 아니라 background prefetch와 H2D 복사까지 포함한, GPU가 다음 batch를 기다린 총시간이다.

병목을 나누어 보려면 다음을 각각 측정한다.

1. `num_workers=0`으로 두고 iterator pull 시간을 측정해 Python transform/로딩 비용을 본다.
2. `.to("cuda")` 주변을 CUDA event 또는 Nsight Systems Copy lane으로 측정해 H2D 비용을 본다.
3. 전체 GPU idle time과 비교한다.

그 결과에 따라 worker·transform을 조정할지, pinned memory·인터커넥트·GDS를 조정할지 결정한다.

### 통신 병목과 연산 병목 구분

gradient all-reduce의 통신량은 보통 모델 파라미터 수에 따라 결정되며 batch size에 직접 비례하지 않는다. 따라서 batch size를 바꿔 compute만 증감시키고 NIC GB/s와 통신 시간 비율을 관찰할 수 있다.

- batch를 줄여도 NIC 처리량이 같은 상한에 머물면 네트워크가 제한 요인일 가능성이 크다.
- batch를 줄였을 때 NIC 처리량도 떨어지면 GPU compute가 NIC에 줄 데이터를 충분히 만들지 못하는 상태일 수 있다.

Nsight Systems에서는 kernel 사이의 긴 빈 구간, NCCL 대기, H2D 대기를 보고, Nsight Compute에서는 개별 kernel의 memory/compute 효율을 본다.

---

## 10. 지속적인 튜닝 절차

성능 설정은 GPU 수, 데이터셋, CUDA/NCCL 버전, 스토리지 구성에 따라 달라진다. 한 번 맞춘 값으로 끝내지 않고 다음을 반복한다.

```text
기준선 설정 → 전체 타임라인 프로파일링 → 가설 수립 → 한두 가지 변경
→ 재측정 → 좋은 설정 기록·자동화
```

1. 단일 GPU에서 `samples/s`, step time, latency 기준선을 잡는다.
2. 단일 노드 다중 GPU, 다중 노드로 단계적으로 확장한다.
3. GPU 수가 N배인데 처리량이 N배에 못 미치면 CPU·I/O·네트워크·동기화 중 원인을 프로파일러로 분리한다.
4. 한 번에 너무 많은 설정을 바꾸지 않는다.
5. 정기 benchmark와 dashboard로 성능 회귀를 탐지한다.
6. 확인된 환경 변수, 버전, topology 의존성을 코드·설정에 문서화한다.

---

## 핵심 정리

1. GPU를 늘릴 때 스토리지 대역폭, CPU 전처리, worker 수도 함께 늘려야 한다.
2. 많은 작은 랜덤 읽기보다 큰 sequential shard 읽기가 일반적으로 유리하다.
3. 데이터는 로컬 NVMe 또는 가까운 고속 스토리지에 두고 node별 shard를 우선 읽는다.
4. GDS는 storage-to-GPU 경로에서 CPU memory bounce buffer를 제거하지만, 모든 환경에서 자동으로 빨라지는 것은 아니므로 측정이 필요하다.
5. `num_workers`, prefetch, pinned memory, 비동기 H2D 전송을 조합해 다음 batch를 미리 준비한다.
6. DALI·NeMo Curator 같은 도구는 online CPU 전처리를 줄이고 데이터 형식을 학습 친화적으로 만드는 데 쓴다.
7. I/O, H2D, CPU transform, NCCL, GPU kernel을 분리해 관측하고, 전체 step time 기준으로 최적화 효과를 검증한다.
