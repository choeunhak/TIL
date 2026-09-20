# Google SRE Book — Chapter 4: Service Level Objectives

원문: https://sre.google/sre-book/service-level-objectives/

---

## 1. 핵심 메시지

서비스를 운영하려면 무엇을 중요하게 볼지, 또 그것을 어떻게 측정하고 판단할지부터 정해야 한다.

Google SRE는 이를 설명할 때 다음 세 용어를 쓴다.

- SLI: Service Level Indicator
- SLO: Service Level Objective
- SLA: Service Level Agreement

---

# Service Level Terminology

## 2. SLI — Service Level Indicator

SLI는 서비스 품질의 한 측면을 숫자로 나타낸 값이다.

대표적인 SLI는 다음과 같다.

- request latency
- error rate
- system throughput
- availability
- durability

원시 데이터는 정해 둔 측정 구간에 모아, 다음과 같은 방식으로 집계할 수 있다.

- 비율
- 평균
- 백분위수

가능하면 SLI는 우리가 알고 싶은 서비스 품질을 직접 측정해야 한다.

직접 측정하기 어렵다면 대리 지표를 사용할 수 있다.

예를 들어 사용자가 느끼는 지연 시간이 중요해도, 실제로는 서버 측 지연 시간만 측정할 수 있을 때가 있다.

---

## 3. Availability

가용성은 사용자가 서비스를 실제로 쓸 수 있는 비율이다.

많은 경우 다음처럼 정의한다.

```text
Availability
=
Successful well-formed requests
/
Total well-formed requests
```

이를 yield라고 부르기도 한다.

스토리지 시스템에서는 가용성뿐 아니라 내구성도 중요한 SLI다.

높은 가용성은 흔히 "nines"로 표현한다.

- 99% → 2 nines
- 99.999% → 5 nines

책은 당시 Google Compute Engine의 공개 가용성 목표인 **99.95%**, 즉 "three and a half nines"를 예로 든다.

---

## 4. SLO — Service Level Objective

SLO는 SLI가 만족해야 하는 목표값 또는 허용 범위다.

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

외부에서 들어오는 HTTP 요청의 QPS는 사용자 수요에 따라 달라지므로, 의미 있는 SLO를 정하기 어렵다.

반면 요청 지연 시간은 시스템 설계와 운영으로 바꿀 수 있으므로 SLO를 세울 수 있다.

QPS와 지연 시간은 서로 영향을 준다. 특정 부하 임계점을 넘으면 성능이 급격히 무너질 수도 있다.

책의 100ms 지연 시간 목표는 예시일 뿐이다. 다만 지연 시간이 길어질수록 사용자 이탈 가능성이 커진다는 점은 분명하다.

---

## 6. SLO를 공개하는 이유

SLO를 공개하면 사용자가 서비스에 어느 정도를 기대해도 되는지 알 수 있다.

명확한 SLO가 없으면 사용자가 제각각 기대치를 만든다.

SLO를 공개하면 서비스가 느리다는 막연한 불만을 줄이는 데도 도움이 된다.

그 결과:

### Over-reliance

실제보다 서비스가 더 reliable하다고 믿고 과도하게 의존할 수 있다.

### Under-reliance

실제보다 서비스가 덜 reliable하다고 생각하고 충분히 사용하지 않을 수 있다.

---

## 7. Global Chubby Planned Outage

Chubby는 Google의 distributed lock service다.

Global Chubby는 실제 장애가 워낙 드물어, 서비스 책임자들이 Chubby는 절대 멈추지 않는다고 여기기 시작했다.

그 결과 Chubby를 쓰는 서비스 중에는 Chubby가 멈췄을 때 제대로 동작하지 않는 것들이 생겼다.

이를 해결하려고 SRE는 Chubby가 SLO를 지키되, 지나치게 크게 넘기지는 않도록 했다.

분기 동안 실제 장애가 너무 적어 가용성이 목표보다 지나치게 높아지면, 의도적으로 통제된 장애를 만들었다.

덕분에 서비스 책임자도 Chubby 장애를 실제로 처리할 수 있게 됐다.

---

## 8. SLA — Service Level Agreement

SLA는 사용자와 서비스 제공자 사이의 명시적 또는 암묵적 약속이다. 여기에는 SLO를 지키거나 지키지 못했을 때의 결과도 담긴다.

예:

- 환불
- 위약금

SLO와 SLA를 구분하는 질문:

```text
SLO를 만족하지 못하면 어떤 명확한 consequence가 발생하는가?
```

명확한 결과가 없다면 대개 SLA가 아니라 SLO다.

---

## 9. SRE와 SLA

SRE는 보통 SLA 자체를 만드는 데 깊이 관여하지 않는다.

SLA는 비즈니스와 제품 측의 결정에 더 가깝기 때문이다.

하지만 SRE는 다음에 관여한다.

- SLI 정의
- SLO를 객관적으로 측정하는 방법
- SLA에 포함된 SLO를 지키도록 운영 지원

Google Search는 일반 사용자와 명시적 SLA를 맺지 않지만, 그래도 SLI와 SLO는 필요하다.

Search가 멈추면 명시적인 SLA 위약금은 없어도 **평판 손상과 광고 매출 감소**라는 실제 손해가 생긴다. 반면 Google for Work 같은 서비스는 사용자와 명시적 SLA를 맺는다.

---

# Indicators in Practice

## 10. What Do You and Your Users Care About?

모니터링 시스템에서 볼 수 있는 모든 지표를 SLI로 삼아서는 안 된다.

사용자가 시스템에서 무엇을 원하는지 먼저 이해하고, 몇 개의 대표 지표만 골라야 한다.

지표가 너무 많으면 중요한 것에 집중하기 어렵고, 너무 적으면 중요한 시스템 동작을 놓칠 수 있다.

---

## 11. User-facing serving systems

대표적인 SLI는 다음과 같다.

- availability
- latency
- throughput

---

## 12. Storage systems

대표적인 SLI는 다음과 같다.

- latency
- availability
- durability

---

## 13. Big data systems

데이터 처리 파이프라인에서는 다음이 중요하다.

- throughput
- end-to-end latency

일부 pipeline에서는 개별 processing stage의 latency도 중요할 수 있다.

---

## 14. Correctness

모든 시스템에서 정확성은 중요하다.

예:

- 올바른 답을 반환했는가?
- 올바른 데이터를 가져왔는가?
- 올바르게 분석했는가?

정확성은 시스템 상태를 보여 주는 중요한 지표지만, 인프라 자체보다 시스템 안의 데이터 속성인 경우가 많다.

---

# Collecting Indicators

## 15. 서버 측과 클라이언트 측 측정

많은 지표는 서버 측에서 자연스럽게 수집할 수 있다.

예:

- 모니터링 시스템
- 주기적인 로그 분석
- HTTP 500 응답 비율

하지만 일부 시스템은 클라이언트 측 계측이 필요하다.

서버 측 지표만 보면, 사용자에게는 영향을 주지만 서버에는 드러나지 않는 문제를 놓칠 수 있기 때문이다.

### Shakespeare 사례

Shakespeare 검색 백엔드의 응답 지연 시간만 재면, 페이지 JavaScript 문제로 사용자가 오래 기다리는 상황을 놓칠 수 있다.

이 경우 browser에서 page가 usable해질 때까지의 시간을 측정하는 것이 사용자 경험에 더 가깝다.

---

# Aggregation

## 16. Aggregation의 한계

원시 측정값을 집계하면 단순해지지만 중요한 정보가 가려질 수 있다.

책의 요청률 예:

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

요청 지연 시간을 평균으로만 보면 꼬리 구간의 동작이 가려질 수 있다.

책의 Figure 4-1에서는 typical request가 약 50 ms에 처리되지만 일부 request는 약 20배 더 느리다.

평균만 보고 모니터링과 알림을 설정하면 이런 꼬리 구간의 변화를 놓칠 수 있다.

---

## 18. Percentile

지표는 평균보다 분포와 백분위수로 보는 편이 유용할 때가 많다.

Latency에서는:

- 50백분위수 → 일반적인 경우
- 99백분위수 또는 99.9백분위수 → 충분히 일어날 수 있는 최악의 경우

를 볼 수 있다.

응답 시간의 편차가 클수록 긴 꼬리 구간이 사용자 경험에 더 큰 영향을 준다.

책은 사용자 연구를 인용해, 사람들이 **응답 시간 편차가 큰 시스템보다 조금 느리더라도 일관된 시스템을 선호하는 경향**이 있다고 설명한다. 일부 SRE 팀은 99.9백분위수처럼 높은 백분위수에 집중하기도 한다.

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

## 20. SLI 정의 표준화

SLI의 공통 정의를 표준화하면 매번 처음부터 다시 정하지 않아도 된다.

책은 다음을 템플릿 구성 요소로 제시한다.

- 집계 구간
- 집계 지역
- 측정 주기
- 포함할 요청
- 데이터 수집 방식
- 데이터 접근 지연 시간

자주 쓰는 지표마다 재사용 가능한 SLI 템플릿을 만들면, 각 SLI의 의미를 더 쉽게 이해할 수 있다.

---

# Objectives in Practice

## 21. 사용자 요구에서 시작

SLO를 단순히 측정하기 쉬운 지표에서 출발해 정해서는 안 된다.

먼저 사용자가 무엇을 중요하게 생각하는지 정하고, 그 동작을 측정할 지표를 골라야 한다.

직접 측정하기 어렵다면 대리 지표를 쓸 수 있다.

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

성능 곡선의 형태가 중요하다면 여러 목표를 둘 수 있다.

예:

```text
90% of Get RPC calls < 1 ms
99% of Get RPC calls < 10 ms
99.9% of Get RPC calls < 100 ms
```

---

## 24. Workload별 SLO

사용자 워크로드가 서로 다르면 워크로드 종류마다 다른 목표를 정할 수 있다.

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

대신 SLO를 지키지 못해도 되는 비율인 오류 예산을 두고, 이를 매일 또는 매주 추적할 수 있다.

경영진은 월간 또는 분기별 평가를 보면 된다.

---

# Choosing Targets

SLO 목표를 정하는 일은 순수한 기술 활동이 아니다. 제품과 비즈니스에 미칠 영향을 함께 고려해야 하고, 다음과 같은 제약 속에서 제품 특성 사이의 균형을 잡아야 할 수도 있다.

- 인력
- 출시 시점
- 하드웨어 확보 가능성
- 예산

SRE는 이 논의에 참여해 각 선택지의 리스크와 실현 가능성을 설명한다.

## 26. 현재 성능만 보고 목표를 정하지 않는다

현재 성능을 그대로 target으로 정하면 문제가 될 수 있다.

현재 성능이 특별한 노력으로 겨우 유지되는 수준이거나, 큰 재설계 없이는 개선하기 어려울 수 있기 때문이다.

---

## 27. 단순하게 유지하기

복잡한 SLI 집계는 시스템 성능의 변화를 가리고 이해도 어렵게 만든다.

---

## 28. 절대적인 목표는 피하기

다음과 같은 절대적 목표는 현실적이지 않다.

- 부하가 무한히 늘어도 지연 시간이 늘지 않음
- 항상 사용할 수 있음

이런 목표는 구축과 운영 비용이 높고, 사용자에게 실제로 필요한 수준보다 과도할 수 있다.

---

## 29. SLO는 가능한 적게 두기

시스템 특성을 충분히 다룰 수 있을 만큼만 SLO를 둔다.

특정 SLO를 근거로 우선순위에 관한 실제 결정을 바꿀 수 없다면, 그 SLO가 필요한지 다시 생각해야 한다.

모든 제품 특성을 SLO로 표현할 수 있는 것도 아니다.

---

## 30. 완벽함은 나중에 다듬기

처음부터 완벽한 SLO를 만들 필요는 없다.

시스템 동작을 이해해 가면서 SLO 정의와 목표를 수정할 수 있다.

처음에는 다소 느슨한 목표로 시작해 점차 강화하는 편이, 지나치게 엄격한 목표를 세웠다가 완화하는 것보다 낫다.

SLO는 SRE와 제품 개발팀의 **업무 우선순위를 정하는 중요한 기준**이어야 한다. 좋은 SLO는 개발팀이 중요한 일에 집중하게 돕지만, 너무 공격적이면 불필요한 무리수를 만들고 너무 느슨하면 제품 품질이 떨어질 수 있다.

---

# Control Measures

## 31. SLI와 SLO로 만드는 제어 루프

책에서 설명하는 제어 루프는 다음과 같다.

1. 시스템의 SLI를 모니터링하고 측정한다.
2. SLI를 SLO와 비교해 조치가 필요한지 판단한다.
3. 조치가 필요하면 목표를 지키기 위해 무엇을 할지 정한다.
4. 조치를 수행한다.

예를 들어 요청 지연 시간이 늘어나 몇 시간 안에 SLO를 지키지 못할 것으로 보인다면:

- 서버가 CPU 병목인지 확인하고
- 부하를 분산하려고 서버를 추가할 수 있다.

SLO가 없으면 언제 action을 취해야 할지 판단하기 어렵다.

---

# SLOs Set Expectations

## 32. SLO는 사용자 기대를 설정한다

SLO를 공개하면 기존 사용자와 잠재 사용자가 서비스 동작에 대해 현실적인 기대를 가질 수 있다.

사용자는 그 서비스가 자신의 사용 사례에 맞는지 판단할 수 있다.

책에서는 다음 예를 든다.

- 매우 높은 내구성과 낮은 비용을 제공하지만 가용성은 조금 낮은 서비스
- 사진 공유 웹사이트에는 맞지 않을 수 있음
- 기록 보관 관리 시스템에는 맞을 수 있음

---

## 33. Safety margin

사용자에게 공개하는 SLO보다 더 엄격한 내부 SLO를 둘 수 있다.

이렇게 하면 만성적인 문제가 외부에 드러나기 전에 대응할 여유가 생긴다.

---

## 34. Don't overachieve

특히 인프라 서비스에서는 사용자가 문서에 적힌 SLO보다 실제 성능에 의존한다.

실제 성능이 문서에 적힌 SLO보다 훨씬 좋으면, 사용자는 그 성능을 당연하게 받아들일 수 있다.

이를 막기 위해 다음과 같은 방법을 사용할 수 있다.

- 의도적으로 가끔 시스템을 오프라인으로 만들기
- 일부 요청을 제한하기
- 부하가 낮아도 시스템이 더 빨라지지 않게 하기

Chubby planned outage가 이 목적의 사례다.

---

## 35. SLO와 투자 판단

시스템이 기대를 얼마나 잘 충족하는지 알면, 어디에 더 투자할지 판단할 수 있다.

- 속도
- 가용성
- 복원력

반대로 서비스가 충분히 잘 동작한다면 다음에 시간을 사용할 수 있다.

- 기술 부채 정리
- 새로운 기능
- 새로운 제품

---

# Agreements in Practice

## 36. SLA를 만들 때

SLA를 만들 때는 비즈니스팀과 법무팀이 위반 시의 결과와 위약금을 정해야 한다.

SRE는 SLA에 담긴 SLO를 실제로 얼마나 쉽게 달성할 수 있는지, 달성 가능성이 어느 정도인지 판단하는 데 도움을 준다.

사용자에게 공개하는 약속은 보수적으로 정하는 편이 좋다.

대상이 넓을수록 잘못 정한 SLA를 나중에 변경하거나 삭제하기 어렵기 때문이다.

---

# 핵심 정리

- SLI는 서비스 품질의 한 측면을 정량적으로 측정한 값이다.
- SLO는 SLI가 만족해야 하는 목표값 또는 범위다.
- SLA는 SLO를 지키거나 지키지 못했을 때의 결과를 포함하는 약속이다.
- 모든 지표를 SLI로 삼지 말고, 사용자가 중요하게 여기는 몇 개의 대표 지표를 골라야 한다.
- 평균보다 분포와 백분위수가 중요한 경우가 많다.
- SLI 정의를 표준화하면 의미가 명확해지고 재사용하기 쉽다.
- SLO는 측정하기 쉬운 지표가 아니라 사용자가 원하는 동작에서 시작해야 한다.
- SLO는 단순하고, 적고, 절대적이지 않아야 한다.
- SLO는 시스템을 관리하는 제어 루프와 엔지니어링 우선순위의 기준이 된다.
- 공개된 SLO는 사용자의 기대를 정하며, 실제 성능이 SLO를 지나치게 크게 넘는 것도 문제가 될 수 있다.
