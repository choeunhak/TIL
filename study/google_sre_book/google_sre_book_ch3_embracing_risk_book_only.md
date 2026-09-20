# Google SRE Book — Chapter 3: Embracing Risk

원문: https://sre.google/sre-book/embracing-risk/

---

## 1. 핵심 메시지

Google SRE는 100% 신뢰성을 목표로 하지 않는다.

극단적인 신뢰성은 비용이 크고, 새로운 기능 개발과 제품 전달 속도를 늦춘다. 또한 사용자는 이동통신망이나 기기처럼 더 불안정한 요소의 영향을 받기 때문에, 높은 신뢰성과 극단적으로 높은 신뢰성의 차이를 체감하지 못할 수 있다.

따라서 SRE는 단순히 uptime을 최대화하기보다 다음 사이의 균형을 맞춘다.

- 서비스가 unavailable해질 위험
- 빠른 혁신
- 효율적인 서비스 운영

---

## 2. Managing Risk

신뢰성을 높이는 비용은 선형적으로 증가하지 않는다.

책에서는 신뢰성을 높이는 비용을 두 가지로 설명한다.

### 2.1 Redundant machine / compute resources

장애나 유지보수 중에도 서비스를 유지하기 위해 중복 자원과 추가 용량이 필요하다.

예를 들어:

- 정기적 또는 예기치 않은 maintenance 중에도 동작할 수 있는 redundant equipment
- data durability를 보장하기 위한 parity code block 저장 공간

### 2.2 Opportunity cost

엔지니어링 자원을 risk 감소에 사용하면, 그만큼 end user에게 직접 보이는 기능이나 새로운 제품 개발에 사용할 수 있는 자원이 줄어든다.

---

## 3. Risk를 continuum으로 보기

SRE는 risk를 연속선으로 본다.

핵심은 서비스가 감수하는 risk를 비즈니스가 감당하려는 risk와 맞추는 것이다.

목표는 서비스를 충분히 신뢰성 있게 만들되, 필요 이상으로 신뢰성을 높이지 않는 것이다.

예를 들어 availability target이 99.99%라면 이를 초과하되 너무 많이 초과하지 않는 것을 목표로 한다.

지나치게 높은 reliability는 다음 기회를 줄일 수 있다.

- 새로운 기능 추가
- technical debt 정리
- operational cost 감소

이런 의미에서 availability target은 minimum이면서 maximum에 가깝게 취급된다.

---

# Measuring Service Risk

## 4. 서비스 risk의 영향

서비스 failure는 다음과 같은 영향을 만들 수 있다.

- user dissatisfaction
- harm 또는 loss of trust
- 직접적 또는 간접적 revenue loss
- brand 또는 reputational impact
- undesirable press coverage

이 요소들을 모두 하나의 metric으로 만들기 어렵기 때문에 Google은 주로 **unplanned downtime**에 집중한다.

---

## 5. Availability

대부분의 서비스에서는 허용 가능한 unplanned downtime 수준을 availability로 표현한다.

대표적인 값:

- 99.9%
- 99.99%
- 99.999%

각각의 추가적인 9는 100% availability에 한 단계 더 가까워지는 것을 뜻한다.

---

## 6. Time-based availability

전통적인 serving system에서는 전체 시간 중 서비스가 사용 가능한 시간의 비율로 availability를 계산한다.

예를 들어 연간 availability target이 99.99%라면 약 52.56분의 downtime을 허용할 수 있다.

---

## 7. Request success rate 기반 availability

Google의 globally distributed service에서는 time-based availability가 의미 없을 수 있다.

Fault isolation 때문에 서비스 전체가 완전히 down되기보다 일부 traffic을 계속 처리하는 경우가 많기 때문이다.

그래서 Google은 많은 서비스에서 availability를 다음처럼 정의한다.

```text
Availability
=
Successful Requests / Total Requests
```

예:

```text
Daily requests: 2.5M
Daily availability target: 99.99%

허용 가능한 errors: 250
```

모든 request가 동일한 가치를 가지지는 않지만, 전체 request에 대한 success rate는 end-user 관점의 unplanned downtime을 근사하는 합리적인 metric이 될 수 있다.

---

## 8. Nonserving system에 적용

Request success rate는 직접 end user request를 처리하지 않는 시스템에도 적용할 수 있다.

예:

- batch
- pipeline
- storage
- transactional system

책에서는 고객 database의 내용을 추출·변환·data warehouse에 삽입하는 batch process를 예로 든다.

성공적으로 처리된 record와 실패한 record의 비율을 사용하면, 지속적으로 실행되지 않는 batch system에서도 availability를 계산할 수 있다.

---

## 9. Availability target의 관리 주기

Google은 흔히 quarterly availability target을 설정하고 이를 weekly 또는 daily 단위로 추적한다.

이를 통해 높은 수준의 availability objective를 유지하면서 의미 있는 deviation을 발견하고 수정한다.

---

# Risk Tolerance of Services

## 10. Risk tolerance 정의

서비스의 risk tolerance를 정하려면 SRE와 product owner가 business goal을 explicit engineering objective로 바꿔야 한다.

Consumer service와 infrastructure service는 product ownership과 client 요구가 다르기 때문에 따로 접근한다.

---

# Identifying the Risk Tolerance of Consumer Services

## 11. Consumer service에서 고려할 질문

- 어떤 availability 수준이 필요한가?
- 다른 종류의 failure가 서로 다른 영향을 주는가?
- service cost를 이용해 risk continuum상의 위치를 정할 수 있는가?
- availability 외에 중요한 metric이 무엇인가?

---

## 12. Target level of availability

Availability target을 정할 때 고려할 요소:

- 사용자가 기대하는 service level
- service가 revenue와 직접 연결되는지
- paid service인지 free service인지
- 경쟁 서비스가 제공하는 service level
- consumer 대상인지 enterprise 대상인지

### Google Apps for Work

Enterprise 사용자는 Gmail, Calendar, Drive, Docs 등을 실제 업무에 사용한다.

Google Apps for Work의 outage는 Google뿐 아니라 이를 업무에 사용하는 기업의 outage가 된다.

책에서는 전형적인 Google Apps for Work service에 대해 다음 예를 든다.

- external quarterly availability target: 99.9%
- 더 강한 internal availability target
- external target을 달성하지 못하면 penalty가 있는 contract

### YouTube

Google이 YouTube를 인수했을 당시 YouTube는 빠르게 성장하고 변화하는 consumer service였다.

당시에는 높은 availability보다 rapid feature development가 더 중요했기 때문에 enterprise product보다 낮은 availability target을 설정했다.

---

## 13. Types of failures

같은 수의 error라도 failure 형태에 따라 business impact는 다를 수 있다.

예:

- 지속적인 낮은 failure rate
- 가끔 발생하는 full-site outage

### Contact management application 사례

책에서는 다음 두 경우를 비교한다.

1. profile picture가 간헐적으로 표시되지 않음
2. 한 사용자의 private contact가 다른 사용자에게 노출됨

첫 번째는 poor user experience이지만, 두 번째는 user trust를 심각하게 훼손할 수 있다.

두 번째 경우에는 debugging과 cleanup 동안 서비스를 완전히 중단하는 것이 적절할 수 있다.

### Planned downtime

과거 Ads Frontend는 정기적인 maintenance window를 사용했다.

대부분의 작업이 normal business hours에 이루어졌기 때문에 정기적인 scheduled outage가 허용 가능하다고 판단했고, 이를 unplanned downtime이 아니라 planned downtime으로 계산했다.

---

## 14. Cost

Cost는 적절한 availability target을 결정할 때 중요한 요소다.

Ads에서는 request success/failure를 revenue와 직접 연결할 수 있기 때문에 trade-off 계산이 가능하다.

책의 예:

```text
Availability target:
99.9% → 99.99%

Increase:
0.09%

Service revenue:
$1,000,000

Value of improved availability:
$1,000,000 × 0.0009
= $900
```

Availability를 한 단계 높이는 비용이 $900보다 작으면 투자할 가치가 있고, 그보다 크면 비용이 예상 revenue 증가를 초과한다.

---

## 15. Internet background error rate

Reliability와 revenue를 직접 연결하기 어려운 경우, 인터넷 ISP의 background error rate를 참고할 수 있다.

Google이 측정한 typical ISP background error rate는 약:

```text
0.01% ~ 1%
```

범위였다.

End-user perspective에서 서비스 error rate를 이 수준 아래로 낮출 수 있다면, 해당 error는 사용자의 인터넷 연결 noise 안에 묻힐 수 있다.

---

## 16. Other service metrics

Risk tolerance는 availability 외의 metric에도 적용할 수 있다.

### AdWords

Google Search에서 speed는 핵심 특성이었다.

AdWords 광고가 search experience를 느리게 만들어서는 안 되었기 때문에 latency requirement가 중요한 engineering goal이었다.

### AdSense

AdSense는 publisher의 페이지에 삽입된 JavaScript의 요청에 따라 contextual ad를 제공한다.

목표는 광고가 third-party page rendering을 크게 늦추지 않도록 하는 것이다.

이 때문에 AdSense는 AdWords보다 수백 milliseconds 더 느리게 응답할 수 있었다.

이 더 느슨한 latency requirement 덕분에 serving resource를 더 적은 geographical location에 집중해 운영 비용을 줄일 수 있었다.

---

# Identifying the Risk Tolerance of Infrastructure Services

## 17. Infrastructure service의 특성

Infrastructure component는 여러 client를 가지며, client마다 요구사항이 다를 수 있다.

책에서는 Bigtable을 예로 든다.

### User-facing client

일부 service는 user request 경로에서 직접 Bigtable을 사용한다.

이 경우 중요한 것은:

- low latency
- high reliability

### Offline analysis client

다른 팀은 Bigtable을 offline analysis, 예를 들어 MapReduce의 repository로 사용한다.

이 경우에는 reliability보다 throughput이 더 중요할 수 있다.

---

## 18. Types of failures

Low-latency user는 Bigtable request queue가 거의 항상 비어 있기를 원한다.

Request가 도착하면 즉시 처리할 수 있어야 하기 때문이다.

반면 offline analysis user는 throughput을 최대화하기 위해 queue가 비어 있지 않기를 원한다.

System이 다음 request를 기다리며 idle 상태가 되는 것을 피해야 하기 때문이다.

따라서 한 종류의 client에게 success인 상태가 다른 client에게 failure가 될 수 있다.

---

## 19. Cost와 service level 분리

서로 다른 client 요구를 비용 효율적으로 만족시키기 위해 infrastructure를 여러 service level로 나눌 수 있다.

Bigtable 예:

### Low-latency cluster

- low latency
- high reliability
- 짧은 queue
- 더 많은 slack capacity
- 더 높은 redundancy

### Throughput cluster

- 높은 utilization
- 더 적은 redundancy
- latency보다 throughput에 최적화

책에서는 throughput cluster가 low-latency cluster 비용의 약 10~50% 수준까지 낮아질 수 있다고 설명한다.

핵심은 infrastructure provider가 명확하게 구분된 service level을 제공하여 client가 자신의 요구에 맞는 risk/cost trade-off를 선택하도록 하는 것이다.

---

## 20. 서로 다른 datastore 선택 사례

책에서는 다음처럼 데이터를 나누는 예를 든다.

- privacy enforcement에 중요한 데이터 → high-availability, globally consistent datastore
- 중요하지 않지만 user experience를 향상시키는 optional data → 더 저렴하고 덜 reliable하며 덜 fresh한 eventually consistent datastore

동일한 hardware/software를 사용해도 다음을 조절해 다른 service guarantee를 제공할 수 있다.

- resource quantity
- redundancy
- geographical provisioning constraint
- infrastructure software configuration

---

## 21. Frontend infrastructure

Google frontend infrastructure는 network edge 근처에서 동작하는 reverse proxy와 load balancing system으로 구성된다.

이 시스템은 end-user connection의 endpoint 역할도 한다.

이 infrastructure에서 request가 application frontend server까지 도달하지 못하면 request는 그대로 사라지므로 매우 높은 reliability가 필요하다.

---

# Motivation for Error Budgets

## 22. Product Development와 SRE의 긴장

Product development는 주로 product velocity를 중요하게 본다.

SRE는 service reliability를 중요하게 본다.

또한 두 팀 사이에는 information asymmetry가 있다.

- developer는 code 작성과 release effort를 더 잘 안다.
- SRE는 production 상태와 reliability를 더 잘 안다.

---

## 23. 대표적인 긴장 지점

### Software fault tolerance

예상하지 못한 event에 software를 얼마나 강하게 만들 것인가?

### Testing

얼마나 많은 testing을 할 것인가?

### Push frequency

모든 push에는 risk가 있다. Push risk를 줄이는 데 얼마나 투자할 것인가?

### Canary duration and size

새 release를 small subset의 workload에서 얼마나 오래, 어느 정도 규모로 test할 것인가?

이런 판단을 negotiation skill, politics, fear, hope에 맡기지 않고 양쪽이 동의하는 objective metric으로 판단하는 것이 목표다.

---

# Forming Your Error Budget

## 24. Error budget

Product team과 SRE는 service SLO를 기반으로 quarterly error budget을 공동 정의한다.

Error budget은 한 분기 동안 서비스가 얼마나 unreliable할 수 있는지를 나타내는 objective metric이다.

책의 운영 방식:

1. Product Management가 SLO를 정의한다.
2. Monitoring system이 실제 uptime을 측정한다.
3. SLO와 실제 uptime의 차이가 남아 있는 unreliability budget이 된다.
4. 실제 uptime이 SLO보다 높은 동안, 즉 error budget이 남아 있는 동안 new release를 진행할 수 있다.

예:

```text
SLO:
99.999% of all queries successfully served per quarter

Error budget:
0.001% failure rate
```

문제로 인해 분기 예상 query의 0.0002%가 실패하면:

```text
0.0002 / 0.001 = 20%
```

즉 quarterly error budget의 20%를 사용한 것이다.

---

# Benefits

## 25. Error budget의 장점

Error budget의 가장 큰 장점은 Product Development와 SRE가 innovation과 reliability 사이의 균형을 같은 기준으로 판단할 수 있다는 점이다.

SLO가 충족되는 동안 release를 계속할 수 있다.

SLO violation이 누적되어 error budget을 모두 사용하면 release를 일시적으로 중단하고 다음에 투자할 수 있다.

- system testing
- resilience improvement
- performance improvement

더 세밀한 방법으로는 다음도 가능하다.

- release 속도를 낮추기
- SLO violation budget이 거의 소진되면 rollback하기

Error budget이 많이 남아 있으면 product developer가 더 많은 risk를 감수할 수 있다.

Budget이 거의 소진되면 product developer 스스로 더 많은 testing이나 낮은 push velocity를 원하게 된다.

Network outage나 datacenter failure도 error budget을 소비한다.

너무 높은 reliability target 때문에 새 기능 출시가 어려운 경우에는 SLO를 완화해 error budget을 늘릴 수도 있다.

---

# Key Insights

- Service reliability 관리는 대부분 risk 관리이며, risk 관리에는 비용이 든다.
- 100%는 일반적으로 올바른 reliability target이 아니다.
- Service profile을 비즈니스가 감수하려는 risk와 맞춰야 한다.
- Error budget은 SRE와 Product Development의 incentive를 맞추고 공동 책임을 강화한다.
- Error budget은 release rate와 production risk를 보다 객관적으로 결정하게 해준다.
