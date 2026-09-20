# Google SRE Book - Chapter 3~4 상세 정리

원문:
- Chapter 3: https://sre.google/sre-book/embracing-risk/
- Chapter 4: https://sre.google/sre-book/service-level-objectives/

---

# Chapter 3. Embracing Risk

## 1. 핵심 메시지

Google SRE의 기본 관점은 단순하다.

> **신뢰성은 높을수록 무조건 좋은 것이 아니다.**

서비스 신뢰성을 높이면 사용자 경험이 좋아지는 면이 있지만, 동시에 비용이 증가하고 개발 속도가 느려질 수 있다.

```text
Reliability ↑
    ↓
Redundancy ↑
Testing ↑
Operational Complexity ↑
Infrastructure Cost ↑
Engineering Cost ↑
Release Velocity ↓
```

따라서 SRE의 목표는:

```text
100% Reliability
```

가 아니라

```text
Business와 User가 필요로 하는
"충분한 Reliability"
```

를 제공하는 것이다.

---

## 2. 왜 100% Reliability를 목표로 하지 않는가?

100%에 가까워질수록 Reliability 개선 비용은 비선형적으로 증가한다.

예를 들어:

```text
99% → 99.9%
```

와

```text
99.99% → 99.999%
```

는 같은 난이도의 개선이 아니다.

후자로 갈수록 훨씬 많은 비용이 필요하다.

---

## 3. Reliability의 두 가지 주요 비용

Google SRE Book에서는 Reliability를 높이는 비용을 크게 두 가지로 볼 수 있다.

### 3.1 Redundant Resource Cost

장애 상황에서도 서비스를 유지하려면 여유 자원이 필요하다.

예:

```text
N+1 Capacity
Multi-Zone
Multi-Region
Replica
Hot Standby
Backup Storage
Extra Network Capacity
Spare Compute
```

예를 들어 평소 트래픽을 처리하는 데 서버가 100대면 충분하더라도 장애를 고려하면:

```text
100대
+
Failover Capacity
+
Maintenance Capacity
+
Traffic Spike Capacity
```

가 필요할 수 있다.

Reliability를 높일수록:

```text
평소에는 사용하지 않는 Resource
```

도 유지해야 한다.

---

### 3.2 Opportunity Cost

더 중요한 비용은 Engineering Opportunity Cost다.

엔지니어가 Reliability를 높이는 작업에 시간을 쓰면 그 시간 동안 다른 기능을 만들 수 없다.

예:

```text
Engineer Time
├─ Retry 설계
├─ Failover 구현
├─ Chaos Testing
├─ Recovery Logic
├─ Replication
└─ Monitoring
```

이 시간을 다음 작업에 사용할 수도 있다.

```text
Feature
Product Improvement
Cost Optimization
Technical Debt
Developer Productivity
```

즉 Reliability는 Product Development와 경쟁하는 자원이다.

---

# 4. Reliability와 Innovation 사이의 Trade-off

Google SRE의 중요한 관점은 다음과 같다.

```text
Reliability
    ↕
Innovation / Velocity
```

Reliability를 지나치게 높이면:

```text
Change를 두려워함
↓
Release Frequency 감소
↓
Feature Delivery 느려짐
↓
Innovation 감소
```

반대로 너무 빠르게 Change를 하면:

```text
Release 증가
↓
Production Risk 증가
↓
Incident 증가
↓
User Experience 악화
```

따라서 적절한 균형점을 찾아야 한다.

---

# 5. Risk를 Binary가 아니라 Continuum으로 보기

Risk를 다음처럼 단순하게 나누지 않는다.

```text
Safe
Unsafe
```

대신 연속선으로 본다.

```text
Low Risk -------------------------------- High Risk

High Reliability                           Lower Reliability
High Cost                                  Lower Cost
Slow Change                                Faster Change
More Redundancy                            Less Redundancy
```

서비스마다 이 선 위에서 적절한 위치가 다르다.

예:

```text
Payment / Authentication / Core DB
→ 낮은 Risk 선호

Recommendation / Analytics / Optional Feature
→ 상대적으로 높은 Risk 허용 가능
```

핵심은:

> **서비스가 감당할 수 있는 Risk 수준을 명시적으로 선택하는 것**

이다.

---

# 6. "Reliable Enough"라는 개념

SRE의 목표는 서비스가:

```text
Unreliable
```

하지 않도록 만드는 것이지만,

동시에:

```text
Needlessly Reliable
```

하게 만드는 것도 피하는 것이다.

예:

```text
Target Availability = 99.9%

Actual Availability = 99.99999%
```

라고 하자.

이 엄청난 초과 성능을 유지하기 위해:

```text
추가 인프라
복잡한 Failover
많은 운영 인력
긴 Test Cycle
Release 제한
```

이 필요하다면 비효율적일 수 있다.

그 자원을:

```text
New Feature
Cost Reduction
Technical Debt
Automation
```

에 투자할 수 있기 때문이다.

---

# 7. Availability Target은 Minimum이면서 Maximum에 가깝다

일반적으로 SLO는:

```text
최소한 이 정도는 해야 한다
```

라고 생각하기 쉽다.

하지만 Google SRE의 사고방식에서는:

```text
Target보다 조금 좋은 정도
```

가 이상적일 수 있다.

너무 많이 초과한다면:

```text
Reliability에 과투자하고 있는가?
```

를 의심해볼 수 있다.

---

# 8. Service Risk를 어떻게 측정할까?

Risk에는 여러 결과가 있다.

```text
User Dissatisfaction
Revenue Loss
Trust Loss
Reputation Damage
Bad Press
Business Impact
```

하지만 이런 요소를 하나의 Metric으로 만들기는 어렵다.

그래서 실무에서는 종종:

```text
Unplanned Downtime
또는
Availability
```

를 Risk의 대표 지표로 사용한다.

---

# 9. Time-based Availability

전통적인 Availability는 다음처럼 계산한다.

```text
Availability
=
Uptime
------
Total Time
```

예를 들어:

```text
Availability = 99.99%
```

라면 1년 동안 허용되는 Downtime은 대략:

```text
52분 34초
```

정도다.

대표적인 값을 보면:

| Availability | 연간 허용 Downtime(대략) |
|---|---:|
| 99% | 3일 15시간 |
| 99.9% | 8시간 46분 |
| 99.99% | 52분 34초 |
| 99.999% | 5분 15초 |

---

# 10. Google에서 Time-based Availability가 애매한 이유

Google 같은 글로벌 서비스는 일부 Region이나 일부 Request만 실패할 수 있다.

예:

```text
US Region      정상
Asia Region    정상
EU Region      일부 장애
```

이 상황에서 서비스 전체를:

```text
UP
또는
DOWN
```

으로 표현하기 어렵다.

그래서 Google에서는 많은 Serving Service에서:

```text
Request-based Availability
```

를 사용한다.

---

# 11. Request-based Availability

기본식:

```text
Availability
=
Successful Requests
-------------------
Total Requests
```

예:

```text
Total Requests = 2,500,000
Failed Requests = 250

Successful Requests = 2,499,750
```

그러면:

```text
Availability
= 2,499,750 / 2,500,000
= 99.99%
```

이다.

이 방식은 실제 사용자 경험에 더 가깝다.

---

# 12. Request Success Rate의 장점

Request 기반 방식은 Serving Service뿐 아니라 다른 시스템에도 적용 가능하다.

### Batch

```text
Successfully processed records
------------------------------
Total records
```

### Data Pipeline

```text
Successfully completed jobs
---------------------------
Total jobs
```

### Storage

```text
Successful reads/writes
-----------------------
Total read/write operations
```

즉:

```text
"성공한 작업 단위 / 전체 작업 단위"
```

로 일반화할 수 있다.

---

# 13. 모든 Request가 같은 중요도를 가지지는 않는다

예:

```text
GET /profile-image
```

실패와

```text
POST /payment
```

실패는 같은 의미가 아니다.

또:

```text
Background polling 실패
```

와

```text
User login 실패
```

도 영향도가 다르다.

따라서 실제 시스템에서는:

```text
Request Type
Criticality
User Impact
Business Value
```

를 고려해야 한다.

---

# 14. Availability Target은 보통 긴 Window에서 관리한다

예를 들어:

```text
Quarterly SLO
```

를 정하고,

운영에서는:

```text
Daily
Weekly
```

단위로 추적할 수 있다.

구조:

```text
Quarterly Objective
       ↓
Weekly Tracking
       ↓
Daily Monitoring
```

큰 목표를 짧은 주기로 계속 관찰하는 방식이다.

---

# 15. Consumer Service의 Risk Tolerance

Consumer Service의 Reliability 목표는 기술팀만 결정해서는 안 된다.

Product Owner와 함께 결정해야 한다.

질문:

```text
사용자는 어느 정도 Availability를 기대하는가?

서비스가 Revenue와 직접 연결되는가?

Paid Service인가?

Free Service인가?

Enterprise 대상인가?

Consumer 대상인가?

경쟁 서비스는 어느 정도 Reliability를 제공하는가?
```

---

# 16. Enterprise vs Consumer

Enterprise Service는 장애가 고객의 업무 중단으로 이어질 수 있다.

예:

```text
Mail
Calendar
Drive
Docs
```

장애가 발생하면:

```text
우리 서비스 장애
+
고객 회사 업무 장애
```

가 된다.

따라서 높은 Reliability가 필요할 수 있다.

---

반면 빠르게 성장 중인 Consumer Service에서는:

```text
Feature Velocity
```

가 더 중요할 수 있다.

따라서 의도적으로 조금 낮은 Availability Target을 선택할 수도 있다.

---

# 17. Failure Type도 중요하다

같은 Error Count라고 해서 같은 Risk는 아니다.

예:

### Case A

```text
0.1% 사용자에게
계속 작은 실패 발생
```

### Case B

```text
전체 사용자에게
짧은 시간 완전 장애
```

두 경우의 총 Error 수가 같더라도:

```text
User Experience
Business Impact
Trust Impact
```

는 다를 수 있다.

---

# 18. Privacy / Security Failure

Availability보다 훨씬 중요한 Failure도 있다.

예:

### Failure A

```text
Profile Picture가 안 보인다.
```

### Failure B

```text
A 사용자의 Private Contact가
B 사용자에게 노출된다.
```

B는 단순 Availability 문제가 아니다.

```text
Privacy
Security
Correctness
Trust
```

문제다.

이 경우:

```text
서비스를 잠시 완전히 중단
```

하는 것이 오히려 올바른 선택일 수 있다.

---

# 19. Planned Downtime과 Unplanned Downtime

모든 Downtime을 동일하게 보지 않을 수도 있다.

예:

```text
Maintenance Window
```

을 미리 공지하고 서비스 특성상 허용할 수 있다면:

```text
Planned Downtime
```

으로 관리할 수 있다.

반대로 예기치 않은 장애는:

```text
Unplanned Downtime
```

이다.

---

# 20. Cost를 이용해 Reliability 목표를 결정하기

Reliability를 한 단계 높일 가치가 있는지 비용으로 판단할 수도 있다.

예:

```text
현재 Availability = 99.9%
목표 Availability = 99.99%
```

개선폭:

```text
0.09%
```

서비스 Revenue:

```text
$1,000,000
```

이라고 단순화하면 추가 Availability의 가치는:

```text
$1,000,000 × 0.0009
= $900
```

이다.

만약 Reliability 개선 비용이:

```text
$50,000
```

이라면 경제적으로 맞지 않을 수 있다.

물론 실제 서비스에서는:

```text
Trust
Brand
Future Revenue
User Retention
```

도 고려해야 하므로 이 계산은 단순 모델이다.

---

# 21. 다른 Metric에 대한 Risk Tolerance

Risk는 Availability만의 문제가 아니다.

예:

```text
Latency
Durability
Freshness
Correctness
Throughput
```

도 중요한 Service Property다.

---

# 22. Latency 사례

두 서비스가 있다고 하자.

### Search Ads

검색 결과와 같이 보여줘야 하므로:

```text
Search 결과보다 광고 때문에 느려지면 안 됨
```

따라서 매우 강한 Latency Requirement가 필요하다.

### Third-party Page Ads

외부 웹페이지에 삽입되는 광고라면:

```text
페이지 전체 Rendering을 크게 방해하지 않는 정도
```

면 충분할 수 있다.

이 경우 더 높은 Latency를 허용할 수 있고,

그 결과:

```text
Region 수 감소
Provisioning 감소
Operational Cost 감소
```

가 가능하다.

---

# 23. Infrastructure Service의 Risk Tolerance

Infrastructure는 일반 Consumer Product와 다르다.

예:

```text
Database
Storage
Queue
Cache
Load Balancer
Kubernetes Platform
```

이런 서비스에는 다양한 Client가 존재한다.

Client별로 요구사항도 다르다.

---

# 24. Low-Latency Client vs Throughput Client

예를 들어 Distributed Storage를 생각해보자.

### Interactive Client

원하는 것:

```text
Low Latency
High Availability
Short Queue
```

### Batch Client

원하는 것:

```text
High Throughput
High Utilization
Low Cost
```

Interactive Service 관점에서는:

```text
Queue가 비어 있는 것
```

이 좋다.

반면 Batch 관점에서는:

```text
항상 Work가 Queue에 있어
Resource가 놀지 않는 것
```

이 좋다.

서로 최적 상태가 다르다.

---

# 25. Service Tier를 나누는 이유

모든 Client에게 최고 Reliability를 제공하는 것은 비싸다.

그래서 Infrastructure를 여러 Tier로 나눌 수 있다.

예:

```text
Tier A
High Availability
Low Latency
High Redundancy
High Cost

Tier B
High Throughput
Lower Redundancy
Higher Latency
Low Cost
```

사용자는 자신의 Requirement에 맞는 Tier를 선택할 수 있다.

---

# 26. Cloud 환경에서의 유사 사례

비슷한 개념은 Cloud에서도 볼 수 있다.

예:

```text
Multi-AZ DB
vs
Single-AZ DB
```

또는:

```text
On-Demand Instance
vs
Spot Instance
```

또는:

```text
Premium Storage
vs
Standard Storage
```

즉:

```text
Reliability / Performance / Cost
```

를 Client가 선택하도록 한다.

---

# 27. Product Developer와 SRE 사이의 긴장

Product Team은 보통:

```text
Velocity
Feature Delivery
Release Frequency
```

를 중요하게 본다.

SRE는:

```text
Reliability
Production Safety
Availability
```

를 중요하게 본다.

그래서 다음과 같은 갈등이 발생한다.

```text
Developer:
"배포합시다."

SRE:
"위험합니다."
```

---

# 28. 대표적인 갈등 지점

### Fault Tolerance

```text
얼마나 많은 예외 상황까지 처리해야 하는가?
```

### Testing

```text
Test를 얼마나 많이 해야 하는가?
```

### Push Frequency

```text
얼마나 자주 배포할 것인가?
```

### Canary

```text
Canary Size는?
Canary Duration은?
```

모두 정답이 하나가 아니다.

---

# 29. 사람의 의견으로만 결정하면 생기는 문제

다음 요소가 결정을 좌우할 수 있다.

```text
경험
직급
정치
목소리 큰 사람
개인의 Risk Tolerance
```

SRE는 이 갈등을 객관화하려 한다.

그 핵심 도구가:

```text
Error Budget
```

이다.

---

# 30. Error Budget

Error Budget은:

> **SLO가 허용하는 실패량**

이다.

예:

```text
Availability SLO = 99.9%
```

이면:

```text
Allowed Error Rate
= 100% - 99.9%
= 0.1%
```

이 0.1%가 Error Budget이다.

---

# 31. Error Budget 공식

```text
Error Budget
=
1 - SLO
```

예:

```text
SLO = 99.99%
```

이면:

```text
Error Budget = 0.01%
```

---

# 32. Request 기반 Error Budget 예시

분기 동안:

```text
Total Requests
= 1,000,000,000
```

SLO:

```text
99.99%
```

Error Budget:

```text
0.01%
```

허용 Error:

```text
1,000,000,000 × 0.0001
= 100,000
```

즉:

```text
분기 동안 100,000개의 실패 Request
```

까지 Budget 내에 있을 수 있다.

---

# 33. Error Budget 소비

Budget:

```text
100,000 errors
```

Incident에서:

```text
20,000 errors
```

발생했다면:

```text
20,000 / 100,000
= 20%
```

즉:

```text
Error Budget 20% 소비
```

이다.

---

# 34. Error Budget과 Release

Budget이 많이 남아 있다면:

```text
Feature Release
Experiment
Refactoring
Architecture Change
```

같은 Change Risk를 더 감수할 수 있다.

```text
Budget 충분
↓
Innovation 가능
```

반대로 Budget이 거의 없다면:

```text
Release 감소
Reliability Work 증가
Testing 강화
Incident Prevention
```

로 전환할 수 있다.

---

# 35. Error Budget Policy 예시

조직에서 다음과 같이 정책화할 수 있다.

```text
Error Budget 100~50%
→ Normal Release

50~20%
→ Release Risk 확인 강화

20~0%
→ Change 제한

0%
→ Reliability 개선 우선
```

이 값 자체는 조직마다 다르다.

핵심은:

```text
감
```

이 아니라

```text
Data
```

로 Release Risk를 결정하는 것이다.

---

# 36. Error Budget이 해결하는 조직 문제

기존 구조:

```text
Developer
"더 빨리 배포하고 싶다."

SRE
"더 안정적으로 해야 한다."
```

Error Budget 적용:

```text
SLO
 ↓
Measured Reliability
 ↓
Error Budget
 ↓
Remaining Budget
 ↓
Release Decision
```

즉 논쟁이:

```text
Opinion
```

에서:

```text
Shared Metric
```

으로 이동한다.

---

# Chapter 3 전체 흐름

```text
100% Reliability는 비효율적
        ↓
서비스마다 적절한 Risk가 존재
        ↓
Risk Tolerance를 정의
        ↓
Availability 등으로 측정
        ↓
SLO 설정
        ↓
Error Budget 계산
        ↓
Reliability와 Release Velocity를 조정
```

---

# Chapter 3 한 줄 요약

> **신뢰성을 무조건 최대화하지 말고, 비즈니스가 감당할 수 있는 위험 수준을 정한 뒤 Error Budget으로 관리하라.**

---

---

# Chapter 4. Service Level Objectives

## 1. Chapter 4의 핵심 질문

서비스를 운영하려면 가장 먼저 알아야 하는 것은:

```text
"이 서비스에서 무엇이 중요한가?"
```

이다.

그리고 다음 질문이 이어진다.

```text
그걸 어떻게 측정하지?

어느 정도면 충분하지?

그 기준을 못 맞추면 어떻게 하지?
```

이 세 질문이 각각:

```text
SLI
SLO
SLA
```

로 연결된다.

---

# 2. SLI / SLO / SLA 전체 관계

```text
User가 중요하게 생각하는 것
          ↓
         SLI
          ↓
      실제 측정값
          ↓
         SLO
          ↓
      목표 수준
          ↓
         SLA
          ↓
위반 시 계약/비즈니스 결과
```

---

# 3. SLI - Service Level Indicator

SLI는:

> **서비스 수준을 나타내는 정량적인 측정값**

이다.

대표적인 SLI:

```text
Availability
Latency
Error Rate
Throughput
Durability
Correctness
```

---

# 4. Availability SLI

예:

```text
Successful Requests
-------------------
Total Requests
```

예:

```text
999,500 successful
1,000,000 total
```

이면:

```text
Availability = 99.95%
```

이다.

---

# 5. Latency SLI

Latency도 대표적인 SLI다.

예:

```text
p50 = 50ms
p95 = 150ms
p99 = 500ms
```

단순 Average 하나보다 Distribution을 보는 것이 중요하다.

---

# 6. Error Rate SLI

예:

```text
Error Rate
=
Failed Requests
---------------
Total Requests
```

예:

```text
Failed = 500
Total = 1,000,000
```

이면:

```text
Error Rate = 0.05%
```

이다.

---

# 7. Throughput SLI

예:

```text
Requests Per Second
Transactions Per Second
Records Processed Per Second
```

특히:

```text
Serving System
Batch System
Data Pipeline
```

에서 중요하다.

---

# 8. Durability SLI

Storage 시스템에서는:

```text
데이터가 장기간 보존되는가?
```

가 중요하다.

예:

```text
Stored Data Loss Probability
```

또는 특정 기간 동안:

```text
Successfully retained objects
```

로 표현할 수 있다.

---

# 9. SLO - Service Level Objective

SLO는:

> **SLI가 달성해야 하는 목표값 또는 목표 범위**

다.

예:

```text
SLI:
Availability

SLO:
Availability ≥ 99.9%
```

또는:

```text
SLI:
Latency

SLO:
99% of requests < 200ms
```

---

# 10. SLA - Service Level Agreement

SLA는:

> **사용자와 서비스 제공자 사이의 서비스 수준 약속**

이다.

보통 SLO 위반에 대한 결과를 포함한다.

예:

```text
Service Credit
Refund
Penalty
Contractual Consequence
```

---

# 11. SLI / SLO / SLA를 간단히 외우는 방법

```text
SLI
What are we measuring?

SLO
What target do we want?

SLA
What happens if we fail?
```

---

# 12. SLI / SLO / SLA 예시

```text
SLI
Availability

Measured Value
99.95%

        ↓

SLO
Availability ≥ 99.9%

        ↓

SLA
Availability < 99.5%
→ Service Credit
```

---

# 13. SLA가 없어도 SLO는 필요하다

모든 서비스가 고객과 계약을 맺는 것은 아니다.

예:

```text
Public Free Service
Internal Platform
Internal API
```

SLA가 없어도:

```text
SLI
SLO
```

는 운영을 위해 매우 유용하다.

---

# 14. 좋은 SLI는 User Experience를 반영해야 한다

Monitoring System에는 많은 Metric이 존재한다.

예:

```text
CPU
Memory
Disk
GC
Thread Count
Network
Queue Depth
Pod Restart
Node Pressure
```

하지만 이것들이 전부 SLI는 아니다.

SRE에서 중요한 것은:

```text
User가 무엇을 경험하는가?
```

다.

---

# 15. Infrastructure Metric과 SLI 구분

예:

```text
CPU = 95%
```

여도:

```text
API Latency 정상
Error Rate 정상
```

이면 사용자에게 문제는 없을 수 있다.

반대로:

```text
CPU = 20%
```

라도:

```text
DB Network 문제
```

때문에 Request가 실패할 수 있다.

따라서:

```text
CPU / Memory
→ Diagnostic Metric

Availability / Latency
→ User-facing SLI
```

로 구분할 수 있다.

---

# 16. User-facing Serving System의 대표 SLI

대표적으로:

```text
Availability
Latency
Throughput
```

질문으로 바꾸면:

```text
요청에 응답했는가?

얼마나 빨리 응답했는가?

얼마나 많은 요청을 처리했는가?
```

이다.

---

# 17. Storage System의 대표 SLI

대표적으로:

```text
Availability
Latency
Durability
```

질문:

```text
데이터를 읽고 쓸 수 있는가?

얼마나 빨리 읽고 쓸 수 있는가?

데이터가 보존되는가?
```

---

# 18. Data Pipeline의 대표 SLI

대표적으로:

```text
Throughput
End-to-End Latency
Correctness
```

질문:

```text
얼마나 많은 데이터를 처리하는가?

입력에서 최종 결과까지 얼마나 걸리는가?

결과가 정확한가?
```

---

# 19. Correctness도 SLI 후보다

다음 요청이 있다고 하자.

```text
HTTP 200
Latency = 20ms
```

하지만 결과가 틀렸다.

예:

```text
GET /balance

HTTP 200

balance = 잘못된 값
```

Availability와 Latency만 보면 정상이다.

하지만 사용자 관점에서는 실패다.

따라서:

```text
Correctness
```

도 서비스에 따라 핵심 Health Indicator가 된다.

---

# 20. 모든 Metric을 SLI로 쓰면 안 된다

너무 많은 SLI를 선택하면:

```text
무엇이 중요한지 불분명
↓
Monitoring 복잡
↓
Priority 판단 어려움
```

이 발생한다.

Google SRE는 보통:

```text
소수의 대표 Indicator
```

를 선택하는 것을 권장한다.

---

# 21. Client-side vs Server-side Measurement

SLI는 어디에서 측정하느냐도 중요하다.

---

## Server-side

```text
Client
  ↓
Network
  ↓
Server [측정]
```

측정 가능한 것:

```text
Backend Latency
HTTP Response Code
Server Error Rate
```

---

## Client-side

```text
[측정] Client
    ↓
Network
    ↓
Server
```

Client 측에서는:

```text
Network
CDN
Frontend Rendering
JavaScript
Backend
```

까지 포함한 실제 사용자 경험을 볼 수 있다.

---

# 22. Proxy Metric의 한계

이상적인 Metric:

```text
Actual User Experience
```

하지만 이것이 어려우면:

```text
Server-side Latency
```

같은 Proxy를 사용할 수 있다.

문제는:

```text
Server Latency
!=
User-perceived Latency
```

라는 것이다.

예:

```text
User Latency
=
DNS
+ Network
+ CDN
+ LB
+ Backend
+ Browser Rendering
```

따라서 가능하면 사용자 경험에 가까운 지표를 선택해야 한다.

---

# 23. JavaScript 문제 예시

Backend Search Latency가:

```text
50ms
```

라고 해도 Browser JavaScript 문제로:

```text
페이지가 5초 뒤에 usable
```

해질 수 있다.

Server-side SLI만 보면 정상이다.

Client-side Metric을 보면 실제 사용자 문제를 발견할 수 있다.

---

# 24. Aggregation은 위험할 수 있다

Raw Metric은 보통 Aggregate해서 본다.

예:

```text
1분 평균 RPS
```

하지만 평균은 Burst를 숨길 수 있다.

예:

### Service A

```text
100
100
100
100
```

### Service B

```text
200
0
200
0
```

평균은 둘 다:

```text
100 RPS
```

이다.

하지만 B는 순간적으로:

```text
200 RPS
```

를 견뎌야 한다.

---

# 25. Average Latency의 문제

예:

```text
95 requests = 50ms
5 requests = 1000ms
```

Average만 보면 크게 나빠 보이지 않을 수 있다.

하지만 5%의 사용자는:

```text
20배 느린 경험
```

을 한다.

그래서 Latency는:

```text
Average
```

보다:

```text
Distribution
Percentile
```

을 보는 것이 중요하다.

---

# 26. Percentile

예:

```text
p50 = 50ms
p95 = 200ms
p99 = 800ms
p99.9 = 2s
```

의 의미:

```text
p50
→ 50% 요청이 50ms 이하

p95
→ 95% 요청이 200ms 이하

p99
→ 99% 요청이 800ms 이하
```

---

# 27. Tail Latency

분산 시스템에서는 Tail Latency가 특히 중요하다.

예:

```text
p50 = 40ms
p99 = 2s
```

대부분 사용자는 빠른 응답을 받지만 일부 사용자는 매우 느린 응답을 받는다.

---

# 28. Fan-out 시스템에서 Tail이 악화되는 이유

하나의 Frontend Request가 여러 Backend에 요청한다고 하자.

```text
Frontend
├─ Auth
├─ Profile
├─ Recommendation
├─ Inventory
└─ Database
```

Frontend가 모든 Backend의 응답을 기다려야 한다면:

```text
가장 느린 Backend
```

가 전체 Request Latency를 결정할 수 있다.

그래서 대규모 Distributed System에서는:

```text
p99
p99.9
```

같은 Tail이 매우 중요하다.

---

# 29. Mean과 Median이 같다고 가정하면 안 된다

컴퓨터 시스템 Metric은 종종 Normal Distribution이 아니다.

예:

```text
Latency < 0ms
```

는 불가능하다.

또:

```text
Timeout = 1000ms
```

이면 성공 Request의 값은 특정 범위에서 잘릴 수 있다.

따라서:

```text
Mean ≈ Median
```

이라고 가정하면 안 된다.

---

# 30. SLI 정의를 표준화하라

같은 이름의 Metric이라도 측정 방법이 다르면 의미가 달라진다.

예:

```text
Latency
```

라고만 하면 부족하다.

다음이 필요하다.

```text
Aggregation Interval
Measurement Frequency
Scope
Request Type
Measurement Location
Latency Definition
```

---

# 31. SLI 정의 예시

예:

```yaml
name: api_latency
request_type: GET
scope: production
measurement_location: server
aggregation_interval: 1m
measurement_frequency: 10s
latency_definition: time_to_last_byte
percentile: p99
```

이렇게 정의하면 팀 간 해석 차이가 줄어든다.

---

# 32. SLI Template을 만들면 좋은 이유

조직에서 다음을 표준화할 수 있다.

```text
HTTP Availability
HTTP Latency
RPC Latency
Storage Durability
Queue Delay
```

각 서비스가 처음부터 Metric 정의를 다시 만들 필요가 없다.

---

# 33. SLO는 User Requirement에서 역산해야 한다

나쁜 접근:

```text
"Prometheus에 이 Metric 있으니까
이걸 SLO로 만들자."
```

좋은 접근:

```text
사용자는 무엇을 중요하게 생각하지?
      ↓
그걸 어떻게 측정하지?
      ↓
SLI 선택
      ↓
SLO 정의
```

즉:

```text
What users care about
```

에서 시작해야 한다.

---

# 34. 좋은 SLO의 조건

나쁜 SLO:

```text
API는 빨라야 한다.
```

좋은 SLO:

```text
30일 Window에서
99% API Request가
200ms 이내에 완료된다.
```

좋은 SLO는 최소한:

```text
Metric
Target
Scope
Measurement Method
Time Window
```

가 명확해야 한다.

---

# 35. 여러 Percentile Target 사용

Latency Distribution 전체를 관리하려면 여러 Target을 둘 수 있다.

예:

```text
90% requests < 100ms
99% requests < 500ms
99.9% requests < 1s
```

이렇게 하면:

```text
Typical User
+
Tail User
```

를 모두 관리할 수 있다.

---

# 36. Workload별 SLO

같은 시스템이라도 Client 종류가 다르면 SLO를 분리할 수 있다.

예:

### Interactive Client

```text
99% requests < 100ms
```

### Batch Client

```text
95% requests < 2s
```

Batch는 Latency보다 Throughput이 중요할 수 있기 때문이다.

---

# 37. SLO 100%를 피해야 하는 이유

예:

```text
100% requests < 100ms
```

는 사실상 단 하나의 Outlier도 허용하지 않는다.

이를 만족시키려면:

```text
Huge Redundancy
Huge Capacity
Very Conservative Release
Complex Architecture
```

가 필요할 수 있다.

따라서:

```text
100%
```

보다는:

```text
99%
99.9%
99.99%
```

등의 목표와 Error Budget을 사용하는 것이 현실적이다.

---

# 38. SLO와 Error Budget

예:

```text
SLO = 99.9%
```

이면:

```text
Error Budget
= 0.1%
```

이다.

관계:

```text
SLI
 ↓
SLO
 ↓
Allowed Failure
 ↓
Error Budget
```

---

# 39. 현재 성능을 그대로 SLO로 정하면 안 된다

현재:

```text
Availability = 99.99%
```

라고 해서:

```text
SLO = 99.99%
```

로 정하면 안 된다.

현재 성능이 다음 때문에 유지되는 것일 수도 있다.

```text
Heroic Manual Work
과도한 Capacity
과도한 Redundancy
Release 제한
```

SLO는:

```text
현재 가능한 성능
```

이 아니라:

```text
User와 Business가 필요한 성능
```

을 기준으로 정해야 한다.

---

# 40. SLO는 단순하게 유지한다

너무 복잡한 SLO:

```text
Region별 Weight
Client별 Weight
API별 Weight
Time별 Weight
복잡한 공식
```

은 아무도 직관적으로 이해하기 어렵다.

좋은 SLO는:

```text
Simple
Understandable
Measurable
Actionable
```

해야 한다.

---

# 41. SLO 개수는 적을수록 좋다

Metric이 200개 있다고 해서:

```text
SLO 200개
```

를 만들 필요는 없다.

대표적으로:

```text
Availability
Latency
Durability
```

몇 개만으로도 충분한 서비스가 많다.

중요한 질문:

```text
"이 SLO를 근거로 Priority를 바꿀 수 있는가?"
```

이다.

그렇지 않다면 그 SLO가 꼭 필요한지 다시 생각해야 한다.

---

# 42. 처음부터 완벽한 SLO를 만들 필요는 없다

실제 서비스 Behavior를 완벽하게 알기는 어렵다.

따라서:

```text
Initial SLO
   ↓
Measure
   ↓
Learn
   ↓
Adjust
```

방식이 현실적이다.

처음에는 비교적 느슨한 Target으로 시작하고 점차 개선할 수 있다.

---

# 43. SLO는 Control Loop의 핵심이다

SLO는 단순 Document가 아니다.

운영 의사결정 도구다.

```text
1. SLI 측정
      ↓
2. SLO와 비교
      ↓
3. Action 필요 여부 판단
      ↓
4. 원인 분석
      ↓
5. Action 수행
```

이것이 Control Loop다.

---

# 44. Control Loop 예시

현재:

```text
p99 Latency
= 250ms
```

SLO:

```text
p99 < 300ms
```

Trend:

```text
250
260
270
280
290...
```

몇 시간 후 SLO 위반 가능성이 있다.

원인 조사:

```text
CPU Saturation
```

확인.

대응:

```text
Replica 추가
```

이 경우 SLO가:

```text
언제 행동해야 하는지
```

판단하는 기준이 된다.

---

# 45. SLO가 없으면 생기는 문제

```text
Latency가 300ms인데
이게 느린 건가?

CPU 85%인데
Scale-out 해야 하나?

Error Rate 0.05%인데
심각한가?
```

판단 기준이 없다.

SLO가 있으면:

```text
현재 수치
vs
목표
```

를 비교해서 의사결정할 수 있다.

---

# 46. SLO는 Engineering Priority를 결정한다

예:

```text
SLO = 99.9%
Actual = 99.99%
```

이면 Reliability에 더 투자하기보다는:

```text
Feature
Cost Optimization
Technical Debt
```

에 시간을 쓰는 것이 합리적일 수 있다.

반대로:

```text
SLO = 99.9%
Actual = 99.5%
```

이면:

```text
Reliability
Incident Reduction
Capacity
Testing
```

이 우선순위가 된다.

---

# 47. SLO는 Expectation Management 도구다

SLO를 공개하지 않으면 사용자들이 스스로 기대치를 만든다.

예:

```text
"이 API는 항상 50ms겠지."

"이 DB는 절대 장애 안 나겠지."
```

실제 시스템과 Expectation이 달라지면 문제가 생긴다.

그래서:

```text
Published SLO
```

는 시스템이 실제로 무엇을 약속하는지 알려주는 역할을 한다.

---

# 48. Over-reliance와 Under-reliance

SLO가 없으면:

### Over-reliance

```text
실제보다 훨씬 Reliable하다고 생각
```

할 수 있다.

### Under-reliance

```text
실제보다 불안정하다고 생각
```

할 수도 있다.

둘 다 시스템 사용 방식에 좋지 않다.

---

# 49. Internal SLO와 External SLO

External 목표보다 내부 목표를 조금 더 높게 둘 수 있다.

예:

```text
External SLO
99.9%

Internal SLO
99.95%
```

이 차이가:

```text
Safety Margin
```

역할을 한다.

구조:

```text
Internal Threshold 위반
       ↓
조기 대응
       ↓
External SLO 위반 방지
```

---

# 50. Don't Overachieve

Infrastructure Service가 SLO보다 지나치게 좋은 성능을 계속 제공하면 사용자는 실제 성능에 의존한다.

예:

```text
Published SLO
99.9%

Actual
99.99999%
```

사용자 입장:

```text
"사실상 절대 장애 안 나네."
```

그러면 Client Architecture가:

```text
Retry 없음
Fallback 없음
Failure Handling 없음
```

으로 변할 수 있다.

결국 드물게 실제 장애가 발생하면 피해가 더 커진다.

---

# 51. Chubby 사례

Google의 Distributed Lock Service인 Chubby는 매우 높은 Reliability를 제공했다.

문제:

```text
실제 장애가 너무 드묾
↓
Client가 장애가 없다고 가정
↓
Failure Handling 구현 안 함
↓
진짜 장애 시 큰 Incident
```

이를 막기 위해 Controlled Outage를 사용해 Client가 실제 Failure를 처리하도록 만들기도 했다.

핵심:

> **실제 Reliability가 SLO를 지나치게 초과하면 잘못된 사용자 기대가 형성될 수 있다.**

---

# 52. SLO는 Trade-off를 가능하게 한다

서비스가 이미 충분히 좋다면:

```text
더 높은 Reliability
```

대신:

```text
Lower Cost
Simpler Architecture
Technical Debt Reduction
New Features
```

를 선택할 수 있다.

즉 SLO는:

```text
"언제 Reliability 개선을 멈춰도 되는가?"
```

에 대한 기준이 된다.

---

# 53. SLA를 만들 때 SRE의 역할

SLA 자체는:

```text
Business
Legal
Product
```

의 영역이 크다.

SRE는:

```text
이 SLO를 실제로 달성 가능한가?

어느 정도 Risk가 있는가?

어떻게 객관적으로 측정할 것인가?
```

를 지원한다.

---

# Chapter 4 전체 흐름

```text
User가 중요하게 생각하는 것
            ↓
           SLI
            ↓
       실제 측정값
            ↓
           SLO
            ↓
       목표 Service Level
            ↓
      Error Budget
            ↓
Engineering / Release Decision
```

---

# Chapter 3 + Chapter 4 연결

두 장은 사실상 하나의 흐름이다.

Chapter 3의 질문:

```text
얼마나 많은 Risk를 허용할 것인가?
```

Chapter 4의 질문:

```text
그 Risk를 어떻게 Metric과 목표로 표현할 것인가?
```

연결하면:

```text
Business Requirement
        ↓
Risk Tolerance
        ↓
SLI
        ↓
SLO
        ↓
Error Budget
        ↓
Release / Reliability Decision
```

---

# 실무 예제: payment-api

서비스:

```text
payment-api
```

사용자가 중요하게 생각하는 것:

```text
결제가 성공하는가?
결제가 빨리 처리되는가?
```

---

## Availability SLI

```text
Successful Payment Requests
---------------------------
Total Valid Payment Requests
```

---

## Latency SLI

```text
p99 payment request latency
```

---

## SLO

```text
Availability
≥ 99.95%

Latency
99% requests < 300ms
```

---

## Error Budget

Availability:

```text
100% - 99.95%
= 0.05%
```

월:

```text
100,000,000 requests
```

라면:

```text
100,000,000 × 0.0005
= 50,000
```

즉:

```text
50,000 failed requests
```

가 Error Budget에 해당한다.

---

# Kubernetes / EKS 관점 예시

Kubernetes 서비스에서는 다음 Metric을 많이 본다.

```text
CPU
Memory
Pod Restart
Node Ready
OOM Kill
Replica Count
```

이 Metric들은 중요하지만 대부분 직접적인 User-facing SLI는 아니다.

더 직접적인 SLI는:

```text
Request Success Rate
p95/p99 Latency
```

다.

구조:

```text
User

 ↓

Load Balancer / Ingress

 ↓

Service

 ↓

Pod

 ↓

Database / Cache
```

사용자는:

```text
Pod Restart Count
```

를 경험하지 않는다.

사용자는:

```text
Request Failure
Slow Response
```

를 경험한다.

따라서:

```text
CPU / Memory / Pod Restart
= Diagnostic / Cause Metrics

Availability / Latency
= User-facing SLI
```

로 구분하면 좋다.

---

# Prometheus 예시

## Availability

```promql
sum(rate(http_requests_total{status!~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

---

## Error Rate

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

---

## p99 Latency

```promql
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket[5m]))
  by (le)
)
```

주의:

실제 SLI에서는 다음을 명확히 정의해야 한다.

```text
어떤 Request를 포함하는가?
4xx는 Error인가?
Retry는 어떻게 처리하는가?
Health Check는 제외하는가?
Region은 어떻게 합치는가?
```

---

# 실무 Checklist

## Risk

- [ ] 서비스가 정말 100% Availability를 필요로 하는가?
- [ ] Reliability 개선 비용을 알고 있는가?
- [ ] Reliability 때문에 Release Velocity를 지나치게 희생하고 있지 않은가?
- [ ] Business가 감당할 Risk 수준이 정의되어 있는가?
- [ ] Failure 종류별 Impact 차이를 고려했는가?
- [ ] Security / Privacy / Correctness Failure를 Availability와 구분했는가?

---

## SLI

- [ ] 사용자 경험과 직접 관련된 Metric인가?
- [ ] Diagnostic Metric과 SLI를 구분했는가?
- [ ] Client-side 측정이 필요한지 검토했는가?
- [ ] Average 대신 Percentile을 봐야 하는가?
- [ ] Measurement Window가 명확한가?
- [ ] Request Scope가 정의되어 있는가?
- [ ] Correctness를 포함해야 하는가?

---

## SLO

- [ ] SLO가 실제로 측정 가능한가?
- [ ] Time Window가 정의되어 있는가?
- [ ] 현재 Performance가 아니라 User Requirement에서 시작했는가?
- [ ] SLO가 지나치게 복잡하지 않은가?
- [ ] SLO 개수가 너무 많지 않은가?
- [ ] 100% 같은 Absolute Target을 피했는가?
- [ ] Internal SLO와 External SLO가 필요한가?

---

## Error Budget

- [ ] Error Budget이 명확히 계산되는가?
- [ ] Budget Consumption을 지속적으로 추적하는가?
- [ ] Budget 상태가 Release Decision에 반영되는가?
- [ ] Budget이 고갈되면 Reliability Work를 우선하는가?
- [ ] Product와 SRE가 같은 기준을 공유하는가?

---

# 핵심 공식

## Availability

```text
Availability
=
Successful Requests
-------------------
Total Requests
```

---

## Error Rate

```text
Error Rate
=
Failed Requests
---------------
Total Requests
```

---

## Error Budget

```text
Error Budget
=
1 - SLO
```

예:

```text
SLO = 99.9%

Error Budget = 0.1%
```

---

## Allowed Errors

```text
Allowed Errors
=
Total Requests × Error Budget
```

---

# 최종 요약

## Chapter 3

> **Reliability는 최대화 대상이 아니라 최적화 대상이다. 서비스가 감당할 수 있는 Risk를 정의하고 Error Budget으로 관리한다.**

```text
Business Risk Tolerance
        ↓
Reliability Target
        ↓
SLO
        ↓
Error Budget
        ↓
Release / Reliability Trade-off
```

---

## Chapter 4

> **사용자가 중요하게 생각하는 Service Behavior를 SLI로 측정하고, 필요한 목표 수준을 SLO로 정의한다.**

```text
User Experience
      ↓
SLI
      ↓
SLO
      ↓
Error Budget
```

---

# Chapter 3~6을 연결하면

```text
Chapter 3
Embracing Risk

"얼마나 실패를 허용할 것인가?"

        ↓

Chapter 4
Service Level Objectives

"그 허용 수준을 어떻게 측정하고 목표로 만들 것인가?"

        ↓

Chapter 5
Eliminating Toil

"반복 운영 작업을 어떻게 줄일 것인가?"

        ↓

Chapter 6
Monitoring Distributed Systems

"서비스 상태와 사용자 영향을 어떻게 관찰할 것인가?"
```

전체 SRE 흐름:

```text
User Expectations
        ↓
Risk Tolerance
        ↓
SLI / SLO
        ↓
Error Budget
        ↓
Monitoring
        ↓
Alert / Incident
        ↓
Engineering
        ↓
Automation
        ↓
Toil Reduction
        ↓
Scalable Reliability
```
