# Google SRE Book - Chapter 5~6 정리

원문: https://sre.google/sre-book/table-of-contents/

---

# Chapter 5. Eliminating Toil

## 1. Toil이란?

SRE에서 **Toil**은 단순히 "하기 싫은 일"을 의미하지 않는다.

프로덕션 서비스를 운영하기 위해 필요한 작업 중 다음 특성을 가지는 일을 Toil이라고 한다.

| 특징 | 의미 | 예시 |
|---|---|---|
| Manual | 사람이 직접 수행 | 수동으로 스크립트 실행 |
| Repetitive | 반복적으로 발생 | 매일 동일 작업 수행 |
| Automatable | 자동화 가능 | 재시작, 배포, 설정 변경 |
| Tactical | 사후 대응적 작업 | 장애 알람 받고 조치 |
| No enduring value | 작업 후 시스템이 개선되지 않음 | 매번 같은 장애 해결 |
| O(n) scaling | 서비스 규모에 비례해 증가 | 서버 10배 → 운영 작업 10배 |

즉,

> **서비스가 성장할수록 사람도 같이 늘어나야 하는 구조라면 Toil일 가능성이 높다.**

예를 들어 서버 장애가 날 때마다 SRE가 직접 서버를 재시작한다면:

```text
장애 발생
   ↓
Alert
   ↓
SRE 확인
   ↓
서버 재시작
```

문제는 해결되지만 **시스템 자체는 전혀 개선되지 않았다.**

반면 다음과 같이 만들었다면:

```text
장애 감지
   ↓
자동 Recovery
   ↓
원인 분석
   ↓
시스템 개선
```

자동 복구 시스템을 만드는 작업은 **Engineering**에 해당한다.

---

## 2. Toil과 Engineering의 차이

Google은 SRE의 업무를 크게 다음처럼 구분한다.

```text
SRE Work
├─ Software Engineering
├─ Systems Engineering
├─ Toil
└─ Overhead
```

### Software Engineering

코드를 작성하거나 시스템을 개선하는 작업.

예:

```text
자동화 도구 개발
배포 시스템 개발
Auto Scaling 개발
장애 자동복구 시스템 개발
Reliability 기능 개발
```

### Systems Engineering

한 번 수행하면 지속적인 효과가 남는 인프라 개선.

예:

```text
Monitoring 구축
Load Balancer 설정 개선
OS Parameter tuning
Architecture 개선
Productionization
```

### Toil

반복적인 운영 작업.

```text
수동 배포
수동 Restart
반복되는 장애 대응
Alert 처리
수동 설정 변경
```

### Overhead

서비스 운영과 직접 관계없는 일반 업무.

```text
회의
채용
교육
성과평가
행정업무
```

중요한 점은 **귀찮은 일 = Toil은 아니라는 것**이다.

예를 들어 오래된 Alert Rule을 싹 정리하는 작업은 귀찮더라도 이후 운영 품질을 지속적으로 개선하므로 Engineering에 가깝다.

---

## 3. Google의 50% Rule

Google SRE의 중요한 원칙 중 하나는

> **SRE 업무 시간의 최소 50%는 Engineering 작업이어야 한다.**

즉:

```text
Engineering ≥ 50%
Toil + Operational Work ≤ 50%
```

Google이 이렇게 제한하는 이유는 **Toil은 방치하면 계속 증가하기 때문**이다.

서비스가 성장하면서:

```text
Traffic 증가
↓
Server 증가
↓
Incident 증가
↓
Alert 증가
↓
운영 작업 증가
↓
SRE가 운영만 함
```

이런 구조가 되면 결국:

```text
SRE ≒ Operations Team
```

이 되어버린다.

SRE의 목표는 반대로:

```text
Service 규모
10배 증가

↓

SRE 인원
10배 증가 X
```

가 가능하도록 시스템을 만드는 것이다.

즉 **서비스 규모보다 SRE 조직 규모가 더 느리게 증가해야 한다.**

---

## 4. Toil이 위험한 이유

Toil 자체가 항상 나쁜 것은 아니다.

소량의 반복 작업은 단순하고 안정적이어서 오히려 편할 수도 있다.

하지만 Toil이 많아지면 문제가 발생한다.

### 개인

```text
Career stagnation
Burnout
Boredom
Low morale
```

### 조직

```text
Engineering 속도 감소
↓
자동화 감소
↓
Toil 증가
↓
더 많은 인력 필요
↓
더 많은 Toil
```

악순환이 생긴다.

특히 SRE가 Toil을 계속 받아주면 개발팀이

```text
"운영 작업은 SRE가 해주는 것"
```

이라고 생각하게 되는 문제도 발생한다.

---

## Chapter 5 핵심

```text
SRE의 목적은 운영을 잘하는 것이 아니다.

운영 작업 자체를
Engineering을 통해 줄이는 것이다.
```

SRE가 반복적으로 같은 일을 하고 있다면 질문해야 한다.

```text
왜 사람이 이 작업을 하고 있지?

↓

자동화할 수 없나?

↓

애초에 이 작업이 필요 없도록
시스템을 설계할 수 없나?
```

---

# Chapter 6. Monitoring Distributed Systems

## 1. Monitoring의 목적

Monitoring은 시스템에서 발생하는 데이터를

```text
Collect
↓
Process
↓
Aggregate
↓
Display
```

하는 과정이다.

예:

```text
Request count
Error count
Latency
CPU
Memory
Server lifetime
```

Monitoring은 단순히 장애 탐지용만은 아니다.

주요 목적은:

```text
1. 장기 Trend 분석
2. 변경 전후 비교
3. Alerting
4. Dashboard
5. 장애 분석 / Debugging
6. Capacity Planning
```

---

## 2. White-box Monitoring vs Black-box Monitoring

### White-box Monitoring

시스템 **내부 상태**를 관찰한다.

예:

```text
CPU
Memory
GC
Thread
DB Connection
Queue size
Cache hit ratio
Logs
Internal metrics
```

즉:

```text
"시스템 내부에서 무슨 일이 일어나고 있는가?"
```

를 본다.

White-box는 아직 사용자 장애로 드러나지 않은 문제나 retry로 감춰진 실패를 발견하는 데 유용하다.

### Black-box Monitoring

사용자 입장에서 시스템을 바라본다.

예:

```text
HTTP 요청 성공 여부
페이지 응답 속도
API 응답
Login 가능 여부
Checkout 가능 여부
```

즉:

```text
"사용자가 서비스를 정상적으로 사용할 수 있는가?"
```

를 보는 것이다.

Black-box monitoring은 **실제 사용자에게 문제가 발생하고 있는지를 확인하는 데 특히 중요하다.**

---

## 3. Symptom vs Cause

Monitoring에서 매우 중요한 구분이다.

### Symptom

사용자가 경험하는 문제.

```text
HTTP 500 증가
Latency 증가
Request 실패
서비스 접속 불가
```

### Cause

그 문제를 발생시킨 내부 원인.

```text
DB Connection 부족
CPU 100%
Network packet loss
잘못된 Deploy
Disk full
```

구조는 다음과 같다.

```text
Cause
 ↓
DB Connection Exhaustion
 ↓
API Error
 ↓
HTTP 500
 ↓
User Impact
```

Google SRE는 **Paging은 가능하면 Cause보다 Symptom을 중심으로 해야 한다**고 본다.

예를 들어:

```text
CPU > 90%
```

만으로 Pager를 울리는 것보다

```text
API Error Rate > SLO
```

가 훨씬 사용자 영향과 직접 연결된다.

---

## 4. The Four Golden Signals

Google SRE Monitoring에서 가장 유명한 개념이다.

서비스를 모니터링할 때 최소한 다음 **4개의 Golden Signals**을 확인하라고 권장한다.

```text
Latency
Traffic
Errors
Saturation
```

### ① Latency

Request를 처리하는 데 걸리는 시간.

```text
Client
   ↓
Request
   ↓
Service
   ↓
Response

Latency = Request → Response 시간
```

예:

```text
p50 = 50ms
p95 = 200ms
p99 = 800ms
```

주의할 점은 **성공 요청과 실패 요청의 latency를 구분해야 한다**는 것이다.

예:

```text
정상 Request = 500ms

DB 연결 실패
↓
HTTP 500 = 5ms
```

평균만 보면 장애 발생 후 오히려 latency가 좋아진 것처럼 보일 수도 있다.

따라서:

```text
Successful Request Latency
Failed Request Latency
```

를 구분해서 볼 필요가 있다.

### ② Traffic

서비스에 들어오는 **Demand**.

서비스마다 기준이 다르다.

Web Service:

```text
Requests/sec
```

Streaming:

```text
Concurrent connections
Network throughput
```

Database:

```text
Queries/sec
Transactions/sec
```

Traffic은 Capacity 및 Saturation과 함께 봐야 한다.

### ③ Errors

실패한 Request의 비율.

가장 단순한 예:

```text
HTTP 500
HTTP 503
```

하지만 Error는 단순 HTTP status만 의미하지 않는다.

#### Explicit Error

명확한 실패.

```text
HTTP 500
HTTP 503
```

#### Implicit Error

Response 자체는 성공처럼 보이지만 실제 결과가 잘못됨.

```text
HTTP 200

but

잘못된 데이터 반환
```

#### Policy Error

서비스 정책/SLO를 위반.

예:

```text
SLO

Latency < 1 sec
```

그런데:

```text
HTTP 200
Latency = 3 sec
```

라면 프로토콜상 성공이지만 서비스 관점에서는 **Error**로 볼 수 있다.

### ④ Saturation

시스템이 얼마나 **가득 차 있는가**.

대표적인 Resource:

```text
CPU
Memory
Disk
Network
Thread
Connection Pool
Queue
```

예:

```text
CPU 90%

Memory 95%

Connection Pool
99 / 100

Disk
980GB / 1TB
```

Saturation은 단순히 현재 사용률만 보는 것이 아니다.

```text
현재 상태
+
미래 예측
```

도 중요하다.

예:

```text
Disk Remaining: 5%

현재 증가 속도 기준

4시간 뒤 Full 예상
```

이런 것도 Saturation Signal이다.

---

## Golden Signals 정리

| Signal | 질문 | 대표 Metric |
|---|---|---|
| Latency | 얼마나 느린가? | p50/p95/p99 |
| Traffic | 얼마나 요청이 들어오는가? | RPS/QPS |
| Errors | 얼마나 실패하는가? | Error Rate |
| Saturation | 얼마나 한계에 가까운가? | CPU/Memory/Queue |

쉽게 외우면:

```text
Latency     → 느린가?
Traffic     → 얼마나 들어오나?
Errors      → 실패하는가?
Saturation  → 꽉 찼나?
```

---

## 5. 평균보다 Tail Latency가 중요하다

분산 시스템에서 **Average latency만 보는 것은 위험하다.**

예:

```text
99% Request → 50ms
1% Request  → 5000ms
```

평균이 괜찮아 보여도 일부 사용자는 매우 느린 요청을 경험할 수 있다.

특히 여러 Backend를 호출하는 시스템에서는 문제가 커진다.

```text
Frontend

├─ API A
├─ API B
├─ API C
├─ API D
└─ API E
```

각 Backend에서 발생하는 작은 Tail Latency가 누적되면서 Frontend 전체의 일반적인 latency 문제로 나타날 수 있다.

그래서 Monitoring에서는:

```text
Average
```

보다

```text
p50
p90
p95
p99
p99.9
```

같은 percentile을 보는 것이 중요하다.

---

## 6. Monitoring Resolution

모든 Metric을 동일한 주기로 수집할 필요는 없다.

예:

```text
CPU
→ 초 단위 측정 필요할 수 있음

Disk Capacity
→ 1~2분 단위도 충분

Availability Probe
→ 서비스 SLO에 맞춰 결정
```

Sampling frequency가 높으면:

```text
Data ↑
Storage ↑
Monitoring Cost ↑
Query Cost ↑
```

가 되기 때문이다.

그래서 다음처럼 내부적으로 높은 Resolution으로 관찰하고 외부에는 Aggregate할 수도 있다.

```text
CPU

1초 Sampling
↓
Histogram/Bucket
↓
1분 Aggregate
↓
Monitoring System
```

---

## 7. Monitoring은 단순해야 한다

Monitoring 시스템도 하나의 Production System이다.

너무 복잡하게 만들면:

```text
Monitoring Complexity
      ↓
Monitoring Failure
      ↓
Alert Failure
      ↓
Incident Detection Failure
```

가 발생할 수 있다.

Google은 특히 **Pager까지 이어지는 Critical Path는 단순해야 한다**고 강조한다.

```text
Problem
↓
Metric
↓
Alert Rule
↓
Pager
↓
SRE
```

이 경로는 누구나 이해할 수 있어야 한다.

---

## 8. 좋은 Alert의 조건

Alert를 만들기 전에 다음 질문을 해야 한다.

```text
이 문제는 긴급한가?

사용자에게 실제 영향을 주는가?

사람이 지금 행동해야 하는가?

그 행동을 자동화할 수 없는가?

내일까지 기다려도 되는 문제인가?

다른 Alert와 중복되지 않는가?
```

특히 핵심 원칙은:

> **Every page should be actionable.**

Pager가 울렸다면 사람이 **실제로 할 일이 있어야 한다.**

---

## 9. 사람이 기계처럼 대응한다면 자동화해야 한다

예를 들어 Pager가 울릴 때마다:

```text
Alert 발생

↓ SRE

kubectl rollout restart deployment xxx
```

를 한다고 하자.

이 대응이 항상 똑같다면:

```text
Alert
↓
Human
↓
Script
```

가 아니라

```text
Alert
↓
Automation
```

으로 바꾸는 게 맞다.

즉:

```text
Predictable response
=
Automation candidate
```

Chapter 5의 Toil 개념과 Chapter 6의 Alerting 철학이 여기서 연결된다.

---

## 10. Alert Fatigue

Alert가 너무 많으면:

```text
Alert
Alert
Alert
Alert
Alert
```

처음에는:

```text
Alert → 즉시 대응
```

하지만 시간이 지나면:

```text
Alert → 또 저거네
```

가 된다.

결국 실제 장애까지 무시하게 될 수 있다.

```text
Noise 증가
↓
Alert 신뢰도 감소
↓
Alert 무시
↓
실제 Incident Detection 지연
```

좋은 Alerting 시스템의 목표는:

```text
High Signal
Low Noise
```

다.

---

# Chapter 5 + Chapter 6 연결

두 Chapter는 하나의 철학으로 연결된다.

```text
Monitoring
↓
Alert
↓
Human Response
↓
반복된다
↓
Toil
↓
Automation / Engineering
↓
Alert 감소
↓
더 안정적인 시스템
```

즉 SRE가 해야 할 일은 단순히

```text
장애를 빨리 해결하는 것
```

에서 끝나는 게 아니다.

궁극적으로는:

```text
장애 발견
↓
장애 대응
↓
Root Cause 분석
↓
Engineering
↓
Automation
↓
같은 장애/Alert 제거
```

가 되어야 한다.

---

# 실무 적용 Checklist

## Toil

- [ ] 반복적으로 사람이 수행하는 운영 작업이 있는가?
- [ ] Script를 사람이 직접 실행하고 있지는 않은가?
- [ ] 동일 Alert에 동일 대응을 반복하고 있지는 않은가?
- [ ] 서비스 규모 증가에 따라 운영 인력이 같이 증가하고 있지는 않은가?
- [ ] 반복 작업을 Automation할 수 있는가?
- [ ] 작업 자체가 필요 없도록 시스템을 개선할 수 있는가?

## Monitoring

- [ ] Latency를 측정하는가?
- [ ] Traffic을 측정하는가?
- [ ] Error Rate를 측정하는가?
- [ ] Saturation을 측정하는가?
- [ ] Average뿐 아니라 p95/p99를 보는가?
- [ ] Black-box Monitoring이 있는가?
- [ ] White-box Monitoring이 있는가?
- [ ] Pager가 실제 User Impact 중심으로 발생하는가?
- [ ] 모든 Page가 Actionable한가?
- [ ] 반복적인 Page 대응을 자동화할 수 있는가?
- [ ] 불필요하거나 아무도 보지 않는 Metric/Alert를 제거하고 있는가?

---

# 한 줄 요약

## Chapter 5

> **사람이 반복적으로 하는 운영 작업(Toil)을 Engineering과 Automation으로 제거하라.**

## Chapter 6

> **Monitoring은 Latency, Traffic, Errors, Saturation을 중심으로 하고, Pager는 실제 사용자 영향이 있으며 사람이 즉시 행동해야 하는 문제에만 울려라.**

## Chapter 5 + 6

```text
Good SRE

≠ 장애를 잘 처리하는 사람

Good SRE

= 장애 대응 자체가 점점 필요 없어지도록
  시스템을 개선하는 사람
```
