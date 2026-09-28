# Chapter 5. GPU-Based Storage I/O Optimizations --- 상세 정리

> 출처: Chris Fregly, *AI Systems Performance Engineering*\
> 범위: Chapter 5 --- GPU-Based Storage I/O Optimizations\
> 목적: GPU가 스토리지와 입력 파이프라인을 기다리지 않도록 데이터 경로
> 전체를 최적화한다.

## 0. 이 장의 핵심 문제

GPU가 아무리 빨라도 입력 데이터가 늦게 도착하면 GPU는 계산을 하지 못하고
기다린다.

``` text
Storage
  ↓
Filesystem / Object Store / Network
  ↓
CPU Data Loader
  ↓
Decode / Tokenization / Augmentation
  ↓
Host Memory
  ↓
H2D Transfer
  ↓
GPU HBM
  ↓
GPU Compute
```

따라서 AI 시스템의 성능은 GPU FLOPS만으로 결정되지 않는다. 스토리지
처리량, 파일 접근 패턴, CPU 전처리, host-to-device 전송까지 전체
파이프라인이 GPU 소비 속도를 따라가야 한다.

이 장의 반복되는 원칙은 다음과 같다.

``` text
GPU를 굶기지 않는다.
→ 데이터를 GPU 가까이에 둔다.
→ 큰 단위로 효율적으로 읽는다.
→ 불필요한 CPU memory copy를 줄인다.
→ I/O / preprocessing / H2D / GPU compute를 겹친다.
→ GPU 수가 늘면 input pipeline도 같이 scale-out한다.
→ end-to-end profiling으로 실제 병목을 찾는다.
```

------------------------------------------------------------------------

## 1. Fast Storage and Data Locality

대규모 학습은 TB\~PB 규모의 데이터를 지속적으로 읽는다. 중요한 것은 SSD
하나의 최대 속도가 아니라 **모든 GPU가 요구하는 aggregate bandwidth**다.

``` text
필요한 총 스토리지 처리량
≈ GPU 수 × GPU 한 장이 소비하는 데이터 속도
```

예를 들어 GPU 하나가 200 MB/s를 필요로 한다면:

``` text
1 GPU   →   200 MB/s
8 GPUs  → 1,600 MB/s ≈ 1.6 GB/s
72 GPUs → 수십 GB/s 규모
```

GPU만 늘리고 스토리지 처리량이 그대로면 어느 순간 GPU를 추가해도
throughput이 늘지 않는다.

### 데이터 지역성

가능하면 데이터를 compute에 가깝게 둔다.

``` text
가까움
↑
Local NVMe
Rack-local NVMe-oF
Parallel filesystem / cache
Remote shared storage
Object storage
↓
멀어짐
```

물리적으로 가까우면 network hop과 공유 자원 경쟁을 줄이고 성능 변동도
줄일 수 있다.

### 노드별 데이터 sharding

분산 학습에서는 데이터셋을 노드별로 미리 나누는 방법을 사용할 수 있다.

``` text
100 TB dataset

Node 0 → local 10 TB
Node 1 → local 10 TB
...
Node 9 → local 10 TB
```

각 노드가 자기 로컬 shard를 주로 읽으면 동일 데이터를 여러 노드가 원격
스토리지에서 반복해서 가져오는 일을 줄일 수 있다.

PyTorch `DistributedSampler`는 각 rank가 epoch마다 서로 다른 데이터
slice를 처리하도록 조정하는 데 사용할 수 있다.

### 지역성만 좋아도 끝나는 것은 아니다

``` text
NVMe는 빠름
   ↓
DataLoader worker 부족
   ↓
전처리 속도 부족
   ↓
GPU idle
```

반대로 worker를 무작정 늘리면 CPU core와 disk I/O contention이 증가한다.
따라서 disk throughput, CPU utilization, worker 수를 같이 봐야 한다.

------------------------------------------------------------------------

## 2. Sequential Versus Random Read Patterns

스토리지는 일반적으로 작은 random read를 반복하는 것보다 큰 contiguous
read에서 높은 throughput을 낸다.

### 작은 파일이 많은 경우

``` text
image1.jpg
image2.jpg
image3.jpg
...
수백만 개
```

각 파일마다 다음 비용이 반복된다.

``` text
open
→ metadata lookup
→ small read
→ close
```

이 경우 순수한 디스크 bandwidth보다 request당 overhead와 metadata 처리
비용이 병목이 될 수 있다.

### 큰 shard로 묶기

책에서 제시하는 방향은 여러 sample을 큰 container/shard에 묶는 것이다.

-   Arrow
-   TFRecord
-   Parquet
-   WebDataset tar
-   binary/database container

``` text
작은 파일 수백만 개
        ↓
큰 shard 여러 개
        ↓
sequential read / read-ahead 효율 증가
```

### I/O 크기와 concurrency

작은 4 KB 요청을 계속 보내는 것보다 큰 요청을 사용하는 편이 request
overhead를 줄이는 데 유리하다. 순차 스트리밍에서는 Linux read-ahead를
키우는 것도 도움이 될 수 있다.

random access가 필요하다면 여러 `pread()`를 병렬화하거나 `io_uring`을
사용해 여러 I/O를 동시에 제출하여 latency를 숨길 수 있다.

------------------------------------------------------------------------

## 3. Tuning NVMe and Filesystem for Throughput

### Linux NVMe / block I/O

NVMe는 Linux의 multiqueue block layer(`blk-mq`)를 사용한다.

확인할 항목:

``` text
/sys/block/<device>/queue/scheduler
/sys/block/<device>/queue/read_ahead_kb
```

빠른 NVMe에서는 `none` 또는 `mq-deadline` 같은 scheduler가 사용될 수
있다.

큰 파일을 순차 스트리밍한다면 read-ahead를 기본값보다 크게 잡아 syscall
overhead를 줄이고 pipeline을 유지할 수 있다.

### PCIe가 병목일 수도 있다

SSD 자체가 빠르더라도 PCIe lane이나 연결 세대가 충분하지 않으면 SSD
성능을 다 쓰지 못한다.

``` text
NVMe SSD
   ↓
PCIe
   ↓
CPU / GPU path
```

단일 SSD로 처리량이 부족하면 여러 SSD를 RAID 0으로 stripe하여 aggregate
throughput을 높이는 방법도 있다.

### filesystem

대규모 동시 I/O 환경에서는 XFS 등이 사용될 수 있다. `noatime`을 사용하면
read 때마다 access time을 기록하는 추가 write를 줄일 수 있다.

### Linux page cache

``` text
Disk → RAM page cache → Application
```

최근 읽은 데이터가 RAM에 남아 있으면 재읽기가 빨라진다.

하지만 dataset이 RAM보다 훨씬 크면 cache entry가 계속 교체되면서 cache
thrashing이 발생할 수 있다.

반대로 dataset 전체 또는 상당 부분을 CPU memory나 unified memory에 올릴
수 있다면 startup 시 preload하여 disk I/O를 줄일 수 있다.

------------------------------------------------------------------------

## 4. PyTorch DataLoader 튜닝

대표적인 구성:

``` python
DataLoader(
    dataset,
    num_workers=N,
    pin_memory=True,
    persistent_workers=True,
    prefetch_factor=...
)
```

GPU 전송:

``` python
batch = batch.to(device, non_blocking=True)
```

### `num_workers`

여러 process가 동시에 read/decode/preprocess를 수행한다.

``` text
worker 적음
→ GPU가 data를 기다림

worker 적절
→ pipeline 유지

worker 너무 많음
→ CPU / storage contention
```

정답은 고정값이 아니라 workload별 측정으로 찾아야 한다.

### `pin_memory=True`

page-locked host memory를 사용한다. GPU DMA가 host memory에서 GPU로
데이터를 옮길 때 유리하다.

### `non_blocking=True`

pinned memory가 source일 때 asynchronous H2D transfer를 활용할 수 있다.

### `persistent_workers=True`

epoch이 바뀔 때 worker process를 반복해서 생성하는 비용을 줄인다.

### `prefetch_factor`

worker가 앞으로 사용할 batch를 미리 준비한다.

너무 작으면 queue가 비고 GPU가 기다릴 수 있고, 너무 크면 host memory
사용량이 커진다.

------------------------------------------------------------------------

## 5. NVIDIA GPUDirect Storage (GDS)

GDS의 핵심은 **storage → GPU 경로에서 host memory bounce buffer를
제거하는 것**이다.

### 일반적인 경로

``` text
NVMe / Storage
      ↓
CPU Host Memory
      ↓
CUDA H2D copy
      ↓
GPU HBM
```

### GDS 경로

``` text
NVMe / NVMe-oF / supported storage
              ↓
        DMA data path
              ↓
           GPU HBM
```

CPU가 완전히 사라지는 것은 아니다. CPU는 I/O 설정과 orchestration을 계속
담당한다. 없어지는 것은 데이터가 CPU memory를 중간 staging buffer로
반드시 통과해야 하는 경로다.

### GPUDirect RDMA와의 차이

``` text
GPUDirect RDMA
Network ↔ GPU memory

GPUDirect Storage
Storage ↔ GPU memory
```

둘 다 host memory bounce buffer를 줄이는 방향이지만 대상이 다르다.

### GDS 구성 요소

-   NVIDIA GPU
-   NVIDIA driver / CUDA Toolkit
-   GDS를 지원하는 storage/filesystem stack
-   `cuFile`
-   `nvidia-fs`
-   적절한 direct I/O / DMA 경로

`cuFileRead`를 사용하면 파일에서 GPU device buffer로 데이터를 읽을 수
있다.

비동기 API:

``` text
cuFileReadAsync
cuFileWriteAsync
```

CUDA stream과 결합하여 storage I/O와 다른 작업을 overlap할 수 있다.

### `O_DIRECT`와 alignment

가능하면 `O_DIRECT`를 이용해 OS page cache를 우회하고 direct DMA path를
사용한다.

alignment가 맞지 않으면 내부적으로 추가 copy가 생기거나 throughput이
낮아질 수 있다.

### 언제 GDS가 큰 효과를 내나?

``` text
CPU가 memcpy 때문에 포화
        ↓
GDS로 host bounce 제거
        ↓
CPU load 감소
        ↓
CPU를 preprocessing 등에 사용 가능
```

반대로 CPU가 원래 충분히 여유롭고 storage 자체가 병목이라면 GDS를 넣어도
end-to-end throughput 차이가 작을 수 있다.

따라서 GDS는 "켜면 무조건 빨라지는 옵션"이 아니라 실제 workload에서
검증해야 한다.

------------------------------------------------------------------------

## 6. Checkpointing GPU State with `cuda-checkpoint`

`cuda-checkpoint`는 실행 중인 CUDA process의 GPU 상태를 CPU process
checkpoint 도구인 CRIU 등과 함께 저장하고 복원하는 방식이다.

대략적인 suspend 과정:

``` text
1. CUDA driver entry point lock
2. outstanding GPU work drain
3. GPU device memory → host allocation
4. GPU resource release
5. CRIU 등이 CPU process state 저장
```

복원:

``` text
GPU reacquire
→ device memory 원래 주소에 복원
→ CUDA context / stream 등 복원
→ unlock
→ 실행 재개
```

중요한 점:

``` text
cuda-checkpoint
≠ PyTorch state_dict checkpoint
≠ sharded model checkpoint
```

서로 대체 관계가 아니라 보완 관계다.

`cuda-checkpoint`는 long-running job의 preemption, migration, fault
tolerance에 활용할 수 있다.

또한 GDS와 달리 checkpoint path는 GPU memory를 storage로 바로 DMA하는
방식이 아니다.

``` text
GPU memory
   ↓
Host memory
   ↓
CRIU checkpoint image
```

따라서 사용 중인 VRAM 크기와 GPU↔host link bandwidth가 suspend 시간에
영향을 준다.

------------------------------------------------------------------------

## 7. Measuring GDS with `gdsio`

NVIDIA는 GDS 경로를 benchmark하기 위한 `gdsio`를 제공한다.

CPU-mediated baseline 예:

``` bash
/usr/local/cuda/gds/tools/gdsio \
  -f /mnt/data/large_file \
  -d 0 -w 4 -s 10G -i 1M -I 0 -x 2
```

GDS path:

``` bash
/usr/local/cuda/gds/tools/gdsio \
  -f /mnt/data/large_file \
  -d 0 -w 4 -s 10G -i 1M -I 0 -x 0
```

책의 예시에서는 동일한 설정에서 CPU-mediated path와 GDS path의
throughput과 latency를 비교한다.

하지만 microbenchmark만 보면 안 된다.

``` text
gdsio throughput
CPU utilization
I/O latency
실제 training step time
GPU idle time
```

까지 같이 봐야 한다.

------------------------------------------------------------------------

## 8. DeepSeek Fire-Flyer File System (3FS)

3FS는 DeepSeek이 AI workload를 위해 만든 분산 filesystem이다.

책에서 강조하는 출발점은 AI workload의 대규모 random read다.

일반적인 page cache가 이런 access pattern에서는 효과가 떨어지거나 cache
관리 자체가 낭비가 될 수 있다.

3FS는 direct file I/O를 사용하고 page cache 개입을 줄이는 방향을 취한다.

### 3FS 주요 구성 요소

``` text
Cluster Manager
Metadata Service
Storage Service
Client
```

이 구성 요소들은 InfiniBand 또는 RoCE 같은 RDMA-capable fabric으로
연결된다.

``` text
Client
  ↓
RDMA fabric
  ↓
Storage Service
  ↓
NVMe
```

metadata는 여러 노드에 shard/replicate되어 scale-out을 지원한다.

### GDS와의 관계

3FS가 보여주는 큰 방향은 **AI workload에 맞게 storage layer 자체를
codesign**하는 것이다.

다만 FUSE 기반 userspace filesystem은 GDS가 요구하는 kernel-level
filesystem integration과 `O_DIRECT` semantics 때문에 그대로 true GDS
path를 제공할 수 없다.

책은 GDS가 필요한 경우 NVMe, NVMe-oF, BeeGFS, WekaFS, IBM Storage Scale,
VAST 등 GDS-enabled kernel filesystem client를 예로 든다.

------------------------------------------------------------------------

## 9. Distributed / Parallel Filesystems and Object Stores

### NFS

NFS는 편리하지만 많은 노드가 한 서버를 동시에 읽으면 server
NIC/storage가 병목이 될 수 있다.

``` text
GPU Node 0 ─┐
GPU Node 1 ─┤
GPU Node 2 ─┼→ Single NFS Server
GPU Node 3 ─┘
```

대규모 cluster에서는 단일 NFS server보다 parallel filesystem이나 cache
layer가 적합할 수 있다.

NFS tuning 예:

``` text
rsize
wsize
noatime
async
attribute / lookup cache
```

책에서는 큰 `rsize/wsize`를 사용해 request overhead를 줄이는 방향을
설명한다.

### Object Storage

S3 같은 object store를 training critical path에서 sample 단위로 직접
읽으면 latency와 request overhead가 문제가 될 수 있다.

대안:

``` text
Object Store
    ↓ staging
Local NVMe
    ↓
Training
```

또는:

``` text
Object Store
    ↓
FSx for Lustre 같은 cache
    ↓
GPU cluster
```

큰 range request와 parallel transfer를 사용하고 `s5cmd` 같은 병렬 도구를
활용할 수 있다.

### Parallel Filesystem

Lustre, GPFS/IBM Storage Scale, Ceph 등의 목적은 여러 storage target을
병렬로 사용해 aggregate throughput을 높이는 것이다.

``` text
Large shard
 ├─ chunk → target 0
 ├─ chunk → target 1
 ├─ chunk → target 2
 └─ chunk → target 3
```

stripe가 고르게 구성되지 않으면 특정 storage node만 과부하가 걸릴 수
있으므로 node별 throughput과 request distribution을 같이 봐야 한다.

------------------------------------------------------------------------

## 10. Replication and Compression

### 데이터 복제

각 compute node에 dataset을 복제하면 remote read를 크게 줄일 수 있다.

장점:

``` text
network I/O 감소
local throughput 활용
```

비용:

``` text
storage capacity 증가
dataset 배포 비용
update 관리 비용
```

즉 저장 공간과 throughput의 trade-off다.

### 압축

압축하면 storage에서 읽는 byte 수가 줄어든다.

``` text
compressed data
   ↓ fewer bytes from storage
decompression
   ↓
training data
```

하지만 decompression CPU/GPU cost가 추가된다.

따라서:

``` text
I/O bottleneck + compute 여유
→ compression이 유리할 수 있음

decompression bottleneck
→ 이득 감소
```

이미지에서는 `nvJPEG` 등을 사용해 decode를 GPU로 옮길 수 있고, 최신
GPU의 decompression 기능도 활용할 수 있다.

핵심은 압축률 자체가 아니라 **end-to-end step time이 줄었는지**다.

------------------------------------------------------------------------

## 11. Tuning the Data Pipeline

실제 input pipeline은 단순 read가 아니다.

``` text
read
 ↓
parse / deserialize
 ↓
decode
 ↓
tokenize / augment
 ↓
collate batch
 ↓
H2D
 ↓
GPU compute
```

어느 단계든 GPU 소비 속도보다 느리면 전체 pipeline을 제한한다.

### Python overhead 줄이기

-   worker process로 Python GIL 영향 줄이기
-   sample 단위 Python loop보다 batch/vectorized 처리
-   C++/Rust 기반 tokenizer 활용
-   `collate_fn`에서 tensor 단위 처리
-   critical path의 과도한 logging/transform 제거

### overlap

이상적인 pipeline:

``` text
시간 ───────────────────────────────→

GPU       [ Compute Batch N       ]
CPU              [ Load/Prep N+1 ]
H2D                       [Copy N+1]
GPU                               [Compute N+1]
```

GPU가 batch N을 계산하는 동안 다음 batch를 미리 준비한다.

`non_blocking=True`만 넣는다고 자동으로 완벽한 overlap이 되는 것은
아니다. source가 pinned memory인지, CUDA stream dependency가 올바른지,
실제 timeline에서 overlap이 발생하는지를 확인해야 한다.

------------------------------------------------------------------------

## 12. Scale Out Workers as GPUs Scale Out

GPU 수만 늘고 loader capacity가 그대로면 input pipeline이 새로운
bottleneck이 된다.

``` text
GPU 1개 → worker N
GPU 8개 → worker N 그대로
              ↓
      GPU들이 data 대기
```

따라서 GPU scale-out과 함께 다음도 같이 검토한다.

``` text
DataLoader workers
CPU cores
storage bandwidth
network bandwidth
prefetch capacity
local cache
```

worker를 무한정 늘리는 것이 아니라 CPU와 storage contention이 생기기
직전의 지점을 profiling으로 찾는다.

------------------------------------------------------------------------

## 13. NVIDIA DALI

DALI는 이미지/비디오 등 multimodal preprocessing을 CPU 최적화 코드 또는
GPU에서 수행할 수 있게 한다.

예:

``` text
decode
crop
resize
normalize
augmentation
```

CPU decode/augmentation가 병목이고 GPU에 여유가 있다면 preprocessing을
GPU로 옮겨 CPU bottleneck을 줄일 수 있다.

다만:

``` text
GPU decode
  ↓
CPU로 다시 복사
  ↓
CPU transform
  ↓
GPU로 다시 복사
```

같은 경로는 오히려 host-device copy를 늘릴 수 있다.

가능하면 GPU 친화적인 pipeline은 GPU 안에서 이어지도록 구성한다.

------------------------------------------------------------------------

## 14. NVIDIA NeMo Curator

NeMo Curator는 대규모 LLM/multimodal dataset을 학습 전에 준비하는 데
사용된다.

대표 작업:

-   cleaning
-   filtering
-   deduplication
-   tokenization
-   shuffle
-   shard 생성
-   품질 관리

핵심 아이디어:

``` text
Training 중 매 epoch 비싼 preprocessing
               ↓
가능한 작업을 offline으로 이동
               ↓
training critical path 단순화
```

즉 storage layout과 data format 자체를 학습 친화적으로 미리 만들어 둔다.

------------------------------------------------------------------------

## 15. Monitoring Storage I/O

병목은 계층별로 나눠서 본다.

### Host / storage

-   `iostat`
-   `iotop`
-   `nvme-cli`
-   `perf`
-   eBPF

### GPU / timeline

-   DCGM
-   Nsight Systems
-   Nsight Compute

### GDS

-   `nsys --trace=gds`
-   cuFile 관련 trace

관찰할 것:

``` text
Disk busy?
CPU preprocessing busy?
DataLoader queue empty?
H2D copy 오래 걸림?
GPU kernel 사이에 빈 구간?
NCCL 대기?
```

------------------------------------------------------------------------

## 16. Communication-bound와 Compute-bound 구분

분산 학습에서 gradient all-reduce 양은 주로 model parameter 수에 영향을
받고, batch size에 직접 비례하지 않는다.

따라서 batch size를 바꿔 compute 양을 변화시키면서 NIC throughput과
communication time을 비교하면 병목을 추론할 수 있다.

``` text
batch 감소
+ NIC가 계속 최대치 근처
→ network/communication bottleneck 가능성

batch 감소
+ NIC throughput도 같이 감소
→ compute가 communication을 충분히 공급하지 못하는 상황 가능성
```

Nsight Systems에서는 kernel 사이의 빈 구간, NCCL, H2D wait를 보고 Nsight
Compute에서는 kernel 자체의 compute/memory efficiency를 본다.

------------------------------------------------------------------------

## 17. Continuous Profiling and Tuning Workflow

책이 반복해서 강조하는 방식은 한 번에 모든 것을 바꾸는 것이 아니다.

``` text
Baseline
  ↓
Profile
  ↓
Bottleneck hypothesis
  ↓
1~2개 변경
  ↓
Re-measure
  ↓
좋은 설정 기록
  ↓
Regression monitoring
```

확장 순서도 단계적으로 본다.

``` text
Single GPU
   ↓
Single-node Multi-GPU
   ↓
Multi-node
```

GPU 수가 N배 증가했는데 throughput이 N배에 가까워지지 않는다면 다음 중
무엇이 제한하는지 분리한다.

``` text
CPU
Storage
H2D
Network
Synchronization
GPU kernel
```

------------------------------------------------------------------------

## 18. Chapter 5 전체 연결

``` text
                    ┌─ Local NVMe
Dataset ─ Storage ──┼─ NVMe-oF
                    ├─ Parallel FS
                    └─ Object Store
                          │
                          ▼
                 Sequential / Sharded I/O
                          │
                 ┌────────┴────────┐
                 │                 │
             CPU path           GDS path
                 │                 │
          Host Memory          GPU HBM
                 │                 │
            async H2D              │
                 └────────┬────────┘
                          ▼
                 Decode / Preprocess
                          │
                    DALI / workers
                          │
                          ▼
                      GPU Compute
```

## Key Takeaways

1.  GPU를 늘리면 storage aggregate bandwidth와 DataLoader capacity도
    같이 늘려야 한다.
2.  작은 random I/O를 반복하기보다 큰 sequential shard가 일반적으로
    효율적이다.
3.  데이터는 가능한 compute 가까이에 두고 node-local sharding/cache를
    활용한다.
4.  GDS는 storage→GPU 경로에서 host memory bounce buffer를 제거하지만
    CPU orchestration까지 제거하는 것은 아니다.
5.  GDS 효과는 workload, I/O size, queue depth, filesystem, NIC에 따라
    달라지므로 실제 step time으로 검증한다.
6.  `cuda-checkpoint`는 process/GPU state checkpoint이며 framework model
    checkpoint와 역할이 다르다.
7.  3FS는 AI workload에 맞춰 storage layer 자체를 codesign하는 사례다.
8.  NFS, object store, parallel filesystem은 규모와 access pattern에
    맞게 선택하고 튜닝해야 한다.
9.  worker, pinned memory, prefetch, asynchronous H2D를 조합해 I/O와
    compute를 overlap한다.
10. DALI와 NeMo Curator를 통해 online preprocessing 부담을 줄일 수 있다.
11. 최적화는 항상 end-to-end profiling과 반복 측정으로 확인한다.
