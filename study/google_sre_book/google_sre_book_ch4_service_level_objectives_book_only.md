# Google SRE Book — Chapter 4: Service Level Objectives

원문: https://sre.google/sre-book/service-level-objectives/

---

## 1. 핵심 메시지

서비스를 관리하려면 어떤 behavior가 중요한지, 그리고 그것을 어떻게 측정하고 평가할지를 이해해야 한다.

Google SRE에서는 다음 개념을 사용한다.

- SLI: Service Level Indicator
- SLO: Service Level Objective
- SLA: Service Level Agreement

---

# Service Level Terminology

## 2. SLI — Service Level Indicator

SLI는 제공되는 service level의 특정 측면을 정량적으로 측정한 값이다.

대표적인 SLI:

- request latency
- error rate
- system throughput
- availability
- durability

Raw data는 measurement window 동안 수집한 뒤 다음과 같은 형태로 aggregate할 수 있다.

- rate
- average
- percentile

가능하면 SLI는 관심 있는 service level을 직접 측정해야 한다.

하지만 직접 측정하기 어렵다면 proxy metric을 사용할 수 있다.

예를 들어 user-facing latency가 더 중요하더라도 실제로는 server-side latency만 측정할 수 있는 경우가 있다.

---

## 3. Availability

Availability는 서비스가 usable한 비율이다.

많은 경우 다음처럼 정의한다.

```text
Availability
=
Successful well-formed requests
/
Total well-formed requests
```

이를 yield라고 부르기도 한다.

Storage system에서는 availability와 함께 durability도 중요한 SLI다.

---

## 4. SLO — Service Level Objective

SLO는 SLI가 만족해야 하는 목표값 또는 범위다.

일반적인 형태:

```text
SLI ≤ target
```

또는:

```text
lower bound ≤ SLI ≤ upper bound
```

책의 Shakespeare search service 예:

```text
Average search request latency < 100 ms
```

---

## 5. 모든 SLI에 SLO를 정할 수 있는 것은 아니다

외부에서 들어오는 HTTP request의 QPS는 사용자 수요에 의해 결정되므로 의미 있는 SLO를 설정하기 어렵다.

반면 request latency는 시스템 설계와 운영으로 영향을 줄 수 있기 때문에 SLO를 설정할 수 있다.

QPS와 latency는 서로 영향을 줄 수 있으며, 특정 load threshold를 넘으면 performance cliff가 나타날 수 있다.

---

## 6. SLO를 공개하는 이유

SLO를 사용자에게 공개하면 서비스가 어떤 수준으로 동작할지에 대한 기대를 설정할 수 있다.

명확한 SLO가 없으면 사용자가 스스로 기대치를 만든다.

그 결과:

### Over-reliance

실제보다 서비스가 더 reliable하다고 믿고 과도하게 의존할 수 있다.

### Under-reliance

실제보다 서비스가 덜 reliable하다고 생각하고 충분히 사용하지 않을 수 있다.

---

## 7. Global Chubby Planned Outage

Chubby는 Google의 distributed lock service다.

Global Chubby는 실제 outage가 매우 드물었기 때문에 service owner들이 Chubby가 절대 down되지 않는다고 가정하기 시작했다.

그 결과 Chubby가 unavailable할 때 제대로 동작하지 않는 dependency가 생겼다.

이를 해결하기 위해 SRE는 Chubby가 SLO를 만족하지만 지나치게 초과하지 않도록 했다.

분기 동안 실제 failure가 충분히 발생하지 않아 availability가 target보다 너무 높으면 controlled outage를 의도적으로 발생시켰다.

이렇게 함으로써 service owner가 Chubby failure를 실제로 처리하도록 만들었다.

---

## 8. SLA — Service Level Agreement

SLA는 사용자와 service provider 사이의 명시적 또는 암묵적인 contract이며, 포함된 SLO를 만족하거나 만족하지 못했을 때의 consequence를 포함한다.

예:

- rebate
- penalty

SLO와 SLA를 구분하는 질문:

```text
SLO를 만족하지 못하면 어떤 명확한 consequence가 발생하는가?
```

명확한 consequence가 없다면 대부분 SLA가 아니라 SLO다.

---

## 9. SRE와 SLA

SRE는 일반적으로 SLA 자체를 만드는 일에는 깊게 관여하지 않는다.

SLA는 business와 product decision에 가깝기 때문이다.

하지만 SRE는 다음에 관여한다.

- SLI 정의
- SLO를 objective하게 측정하는 방법
- SLA에 포함된 SLO를 위반하지 않도록 운영 지원

Google Search는 일반 사용자와 명시적 SLA를 맺지 않지만, 그렇더라도 SLI와 SLO는 필요하다.

---

# Indicators in Practice

## 10. What Do You and Your Users Care About?

Monitoring system에서 추적 가능한 모든 metric을 SLI로 사용해서는 안 된다.

사용자가 시스템에서 무엇을 원하는지 이해한 뒤 몇 개의 대표 indicator를 선택해야 한다.

Indicator가 너무 많으면 중요한 metric에 집중하기 어렵고, 너무 적으면 중요한 system behavior를 놓칠 수 있다.

---

## 11. User-facing serving systems

대표적인 SLI:

- availability
- latency
- throughput

---

## 12. Storage systems

대표적인 SLI:

- latency
- availability
- durability

---

## 13. Big data systems

Data processing pipeline 같은 시스템에서는 다음이 중요하다.

- throughput
- end-to-end latency

일부 pipeline에서는 개별 processing stage의 latency도 중요할 수 있다.

---

## 14. Correctness

모든 시스템은 correctness를 중요하게 봐야 한다.

예:

- 올바른 answer를 반환했는가?
- 올바른 data를 가져왔는가?
- 올바른 analysis를 수행했는가?

Correctness는 system health의 중요한 indicator지만, infrastructure 자체보다 system 안의 data property인 경우가 많다.

---

# Collecting Indicators

## 15. Server-side와 client-side measurement

많은 indicator는 server-side에서 자연스럽게 수집할 수 있다.

예:

- monitoring system
- periodic log analysis
- HTTP 500 response 비율

하지만 일부 시스템은 client-side instrumentation이 필요하다.

Server-side metric만 보면 사용자에게 영향을 주지만 server에는 나타나지 않는 문제를 놓칠 수 있기 때문이다.

### Shakespeare 사례

Shakespeare search backend의 response latency만 측정하면 page JavaScript 문제로 인한 poor user latency를 놓칠 수 있다.

이 경우 browser에서 page가 usable해질 때까지의 시간을 측정하는 것이 사용자 경험에 더 가깝다.

---

# Aggregation

## 16. Aggregation의 한계

Raw measurement를 aggregate하면 단순해지지만 중요한 정보를 숨길 수 있다.

책의 request rate 예:

```text
System A:
100 requests/s 계속 유지

System B:
200 requests/s
0 requests/s
200 requests/s
0 requests/s
...
```

두 시스템의 average는 모두 100 requests/s다.

하지만 System B는 순간적으로 두 배의 load를 처리해야 한다.

---

## 17. Average latency의 한계

Request latency를 average로만 보면 tail behavior를 숨길 수 있다.

책의 Figure 4-1에서는 typical request가 약 50 ms에 처리되지만 일부 request는 약 20배 더 느리다.

Average만 기반으로 monitoring과 alerting을 하면 이런 tail 변화가 보이지 않을 수 있다.

---

## 18. Percentile

Metric은 average보다 distribution과 percentile로 보는 것이 유용한 경우가 많다.

Latency에서는:

- 50th percentile → typical case
- 99th 또는 99.9th percentile → plausible worst case

를 볼 수 있다.

Response time variance가 클수록 long-tail behavior가 사용자 경험에 더 영향을 준다.

---

## 19. Statistical fallacies

Google은 일반적으로 mean보다 percentile 사용을 선호한다.

Computer system의 data는 인위적인 제약 때문에 skewed되어 있는 경우가 많다.

예:

- response time은 0 ms보다 작을 수 없음
- timeout이 1,000 ms이면 성공 response는 그보다 큰 값을 갖지 못함

따라서 mean과 median이 같다고 가정하거나, 확인 없이 normal distribution을 가정해서는 안 된다.

---

# Standardize Indicators

## 20. SLI definition 표준화

SLI의 공통 definition을 표준화하면 매번 처음부터 다시 정의할 필요가 없다.

책에서는 다음을 example template 요소로 제시한다.

- Aggregation interval
- Aggregation region
- Measurement frequency
- Included requests
- Data acquisition
- Data-access latency

각 common metric에 reusable SLI template을 만들면 individual SLI의 의미를 더 쉽게 이해할 수 있다.

---

# Objectives in Practice

## 21. 사용자 요구에서 시작

SLO는 단순히 측정 가능한 metric에서 시작해서는 안 된다.

먼저 사용자가 무엇을 중요하게 생각하는지 정하고, 그 behavior를 측정할 indicator를 선택해야 한다.

직접 측정하기 어렵다면 proxy를 사용할 수 있다.

---

# Defining Objectives

## 22. SLO를 명확하게 정의

SLO는 다음을 명확히 해야 한다.

- 어떻게 측정되는지
- 어떤 조건에서 유효한지

책의 예:

```text
99% of Get RPC calls
will complete in less than 100 ms
```

---

## 23. 여러 target 사용

Performance curve의 형태가 중요하다면 여러 target을 지정할 수 있다.

예:

```text
90% of Get RPC calls < 1 ms
99% of Get RPC calls < 10 ms
99.9% of Get RPC calls < 100 ms
```

---

## 24. Workload별 SLO

사용자 workload가 서로 다르면 workload class마다 다른 objective를 설정할 수 있다.

책의 예:

```text
95% of throughput clients' Set RPC calls < 1 s

99% of latency clients' Set RPC calls
with payloads < 1 kB
< 10 ms
```

---

## 25. 100% target을 피하기

SLO를 100% 시간 동안 만족시키겠다는 목표는 현실적이지도 바람직하지도 않다.

이는 다음으로 이어질 수 있다.

- innovation rate 감소
- deployment rate 감소
- 비싸고 지나치게 보수적인 solution

대신 SLO를 miss할 수 있는 비율인 error budget을 허용하고 daily 또는 weekly basis로 추적할 수 있다.

Management는 monthly 또는 quarterly assessment를 볼 수 있다.

---

# Choosing Targets

## 26. Target을 current performance에서 고르지 않는다

현재 성능을 그대로 target으로 정하면 문제가 될 수 있다.

현재 성능이 heroic effort를 요구하거나 큰 redesign 없이는 개선하기 어려운 상태일 수 있기 때문이다.

---

## 27. Keep it simple

복잡한 SLI aggregation은 system performance의 변화를 숨길 수 있고 이해하기 어렵다.

---

## 28. Avoid absolutes

다음과 같은 절대적 목표는 현실적이지 않다.

- load가 무한히 증가해도 latency가 늘지 않음
- 항상 available함

이런 목표는 구축과 운영 비용이 높고, 사용자에게 실제로 필요한 수준보다 과도할 수 있다.

---

## 29. Have as few SLOs as possible

System attribute를 충분히 다룰 수 있을 만큼만 SLO를 정한다.

특정 SLO를 근거로 priority에 관한 실제 결정을 바꿀 수 없다면, 그 SLO가 필요한지 다시 생각해야 한다.

모든 product attribute를 SLO로 표현할 수 있는 것도 아니다.

---

## 30. Perfection can wait

처음부터 완벽한 SLO를 만들 필요는 없다.

System behavior를 배우면서 SLO definition과 target을 수정할 수 있다.

처음에는 느슨한 target으로 시작해 점차 강화하는 편이, 너무 엄격한 target을 설정했다가 완화하는 것보다 낫다.

---

# Control Measures

## 31. SLI와 SLO를 이용한 control loop

책에서 설명하는 control loop:

1. System의 SLI를 monitor하고 measure한다.
2. SLI를 SLO와 비교하고 action이 필요한지 결정한다.
3. Action이 필요하면 target을 충족하기 위해 무엇을 해야 할지 판단한다.
4. Action을 수행한다.

예를 들어 request latency가 증가해 몇 시간 안에 SLO를 miss할 것으로 보인다면:

- server가 CPU-bound인지 test하고
- load를 분산하기 위해 server를 추가할 수 있다.

SLO가 없으면 언제 action을 취해야 할지 판단하기 어렵다.

---

# SLOs Set Expectations

## 32. SLO는 사용자 기대를 설정한다

SLO를 공개하면 사용자와 prospective user가 service behavior에 대해 현실적인 기대를 가질 수 있다.

사용자는 해당 service가 자신의 use case에 적합한지 판단할 수 있다.

책에서는 다음 예를 든다.

- 매우 높은 durability와 low cost를 제공하지만 availability가 조금 낮은 service
- photo-sharing website에는 적합하지 않을 수 있음
- archival records management system에는 적합할 수 있음

---

## 33. Safety margin

User에게 공개하는 SLO보다 더 엄격한 internal SLO를 둘 수 있다.

이를 통해 chronic problem이 외부에 드러나기 전에 대응할 여유를 만들 수 있다.

---

## 34. Don't overachieve

특히 infrastructure service에서는 user가 문서에 적힌 SLO보다 실제 성능에 의존한다.

실제 성능이 stated SLO보다 훨씬 좋으면 사용자는 그 성능을 당연하게 받아들일 수 있다.

이를 막기 위해 다음과 같은 방법을 사용할 수 있다.

- 의도적으로 가끔 system을 offline으로 만들기
- 일부 request를 throttle하기
- light load에서도 system이 더 빨라지지 않도록 하기

Chubby planned outage가 이 목적의 사례다.

---

## 35. SLO와 투자 판단

System이 expectation을 얼마나 잘 충족하는지 알면 다음에 더 투자해야 할지 판단할 수 있다.

- speed
- availability
- resilience

반대로 서비스가 충분히 잘 동작한다면 다음에 시간을 사용할 수 있다.

- technical debt 정리
- 새로운 feature
- 새로운 product

---

# Agreements in Practice

## 36. SLA를 만들 때

SLA를 만들 때는 business와 legal team이 breach의 consequence와 penalty를 정해야 한다.

SRE는 SLA에 포함된 SLO를 실제로 얼마나 쉽게 또는 어렵게 달성할 수 있는지, 그리고 그 가능성이 어느 정도인지 판단하는 데 도움을 준다.

사용자에게 공개하는 promise는 보수적으로 정하는 것이 좋다.

대상이 넓을수록 잘못 정한 SLA를 나중에 변경하거나 삭제하기 어렵기 때문이다.

---

# 핵심 정리

- SLI는 제공되는 service level의 한 측면을 정량적으로 측정한 값이다.
- SLO는 SLI가 만족해야 하는 목표값 또는 범위다.
- SLA는 SLO를 만족하거나 만족하지 못했을 때의 consequence를 포함하는 agreement다.
- 모든 metric을 SLI로 사용하지 말고, 사용자가 중요하게 생각하는 몇 개의 representative indicator를 선택해야 한다.
- Average보다 distribution과 percentile이 중요한 경우가 많다.
- SLI definition을 표준화하면 의미가 명확해지고 재사용이 쉬워진다.
- SLO는 측정하기 쉬운 metric이 아니라 사용자가 원하는 behavior에서 시작해야 한다.
- SLO는 단순하고, 적고, absolute하지 않아야 한다.
- SLO는 system을 관리하는 control loop와 engineering priority의 기준이 된다.
- 공개된 SLO는 user expectation을 설정하며, 실제 성능이 SLO를 지나치게 초과하는 것도 문제가 될 수 있다.
