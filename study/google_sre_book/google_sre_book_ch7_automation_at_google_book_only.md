# Google SRE Book — Chapter 7: The Evolution of Automation at Google

원문: https://sre.google/sre-book/automation-at-google/

---

## 1. 핵심 메시지

SRE에서 automation은 **force multiplier**이지만 만능 해결책은 아니다.

생각 없이 automation을 적용하면 문제를 해결하는 만큼 새로운 문제를 만들 수도 있다.

Google SRE의 관점에서는:

- manual operation보다 software-based automation이 대체로 낫고
- automation보다 더 좋은 것은
- 애초에 manual operation이나 외부 automation이 필요 없는 **autonomous system**이다.

Automation의 가치는 무엇을 자동화하느냐뿐 아니라 **어디에, 어떻게 적용하느냐**에서 나온다.

---

# The Value of Automation

## 2. Consistency

Manual operation은 반복될수록 동일하게 수행되기 어렵다.

사람이 같은 작업을 수백 번 수행하면:

- 실수
- 누락
- data quality 문제
- reliability 문제

가 생길 수 있다.

잘 정의된 procedure를 일관되게 수행한다는 점이 automation의 중요한 가치다.

---

## 3. A Platform

Automation은 consistency뿐 아니라 reusable platform을 제공할 수 있다.

잘 설계된 automation platform은:

- 더 많은 system에 적용할 수 있고
- 새로운 task를 추가할 수 있고
- 같은 bug를 한 번 수정하면 전체에 반영할 수 있고
- 사람이 수행하기 어려운 빈도로 실행할 수 있고
- 사람이 일하기 불편한 시간에도 실행할 수 있고
- process 자체에 대한 metric을 제공할 수 있다.

Manual operation은 scale하거나 확장하기 어렵고, 시스템 운영에 지속적인 비용을 부과한다.

---

## 4. Faster Repairs

Automation이 common fault를 자동으로 해결하면 MTTR을 줄일 수 있다.

Production에서 발견된 문제는 제품 lifecycle 후반에 발견되기 때문에 수정 비용이 크다.

문제가 생기자마자 이를 찾아 자동으로 복구하는 시스템은 전체 운영 비용을 낮출 수 있다.

---

## 5. Faster Action

Infrastructure operation에서는 사람이 machine보다 빠르게 대응하기 어렵다.

Failover나 traffic switching처럼 명확하게 정의할 수 있는 작업은 사람이 개입할 이유가 적다.

Google의 많은 서비스는 이미 manual operation으로 관리할 수 있는 규모를 넘어섰기 때문에 automation 없이는 오래 운영되기 어렵다.

---

## 6. Time Saving

Automation의 대표적인 이유는 time saving이다.

하지만 automation을 작성하는 데 드는 시간과 manual operation에서 절약되는 시간만 비교하면 가치를 과소평가할 수 있다.

한 번 task를 automation으로 만들면 **누구나 같은 operation을 수행할 수 있다.**

즉 operator와 operation을 분리하는 것이 중요한 가치다.

---

# The Value for Google SRE

## 7. Google이 automation을 선호하는 이유

Google의 service는 매우 큰 규모로 운영되기 때문에 개별 machine이나 service를 사람이 직접 관리하기 어렵다.

대규모 환경에서는 특히 다음이 중요하다.

- consistency
- quickness
- reliability

Google의 production environment는 복잡하지만 비교적 uniform하고, 필요한 경우 vendor가 제공하지 않는 API도 직접 구축해왔다.

단기적으로 software를 구매하는 것이 더 저렴하더라도 장기적으로 automation 가능한 API를 확보하기 위해 자체 solution을 개발한 경우도 있다.

Google SRE는 가능한 경우 platform을 만들거나, 시간이 지나 platform으로 발전할 수 있는 방향을 선택해왔다.

---

# The Use Cases for Automation

## 8. 일반적인 automation 사례

책에서는 다음 사례를 든다.

- user account creation
- service cluster turnup / turndown
- software 또는 hardware 설치 준비 및 decommissioning
- new software version rollout
- runtime configuration change
- dependency change

Automation은 software가 software에 작용한다는 의미에서 **meta-software**라고 볼 수 있다.

---

# Google SRE’s Use Cases for Automation

## 9. SRE automation의 초점

Google SRE는 주로 infrastructure lifecycle 관리에 automation을 사용한다.

예:

- new cluster에 service deployment
- system rollout
- configuration change
- service lifecycle 관리

SRE는 infrastructure 위를 흐르는 data의 세부 품질을 직접 관리하기보다 infrastructure 자체를 안정적으로 운영하는 데 더 집중한다.

---

## 10. Abstraction level의 trade-off

Perl 같은 general-purpose language는 매우 낮은 수준의 primitive를 제공하지만 automation 범위가 넓다.

Chef, Puppet 같은 tool은 더 높은 수준의 abstraction을 제공한다.

높은 abstraction은 관리하고 이해하기 쉽지만 **leaky abstraction** 문제가 생길 수 있다.

예를 들어 new binary rollout이 atomic하다고 가정해도 실제로는:

- network failure
- machine failure
- cluster management layer failure
- binary가 staging만 되고 push되지 않음
- push됐지만 restart되지 않음
- restart됐지만 verification되지 않음

같은 partial state가 발생할 수 있다.

---

# A Hierarchy of Automation Classes

## 11. Automation의 진화 단계

이상적인 시스템에서는 외부 glue logic도 필요하지 않다.

책은 database failover를 예로 automation 진화 단계를 설명한다.

1. **No automation**
   - database master failover를 사람이 직접 수행

2. **Externally maintained system-specific automation**
   - SRE 개인 directory에 failover script가 있음

3. **Externally maintained generic automation**
   - 공용 generic failover script에 database support 추가

4. **Internally maintained system-specific automation**
   - database 자체에 failover script 포함

5. **Systems that don’t need any automation**
   - database가 문제를 감지하고 스스로 failover

Google SRE는 가능한 한 마지막 단계인 autonomous system을 지향한다.

---

## 12. Infrequent automation의 문제

Core system과 별도로 유지되는 turnup automation은 underlying system이 바뀌어도 같이 바뀌지 않아 **bit rot**이 발생할 수 있다.

또한 중요한 automation이 드물게 실행되면 test하기 어렵고 feedback cycle이 길어 fragile해진다.

Cluster failover가 대표적인 사례다.

---

# Automate Yourself Out of a Job: Automate ALL the Things!

## 13. Ads Database와 MySQL

오랫동안 Google Ads의 data는 MySQL에 저장됐다.

2005~2008년 Ads Database는 비교적 mature한 상태였고, standard replica replacement의 많은 부분이 이미 자동화돼 있었다.

팀은 그다음 단계로 MySQL을 Google cluster scheduler인 **Borg** 위로 이동하려 했다.

목표는 두 가지였다.

- machine / replica maintenance 제거
- 여러 MySQL instance를 같은 physical machine에 배치하여 resource utilization 개선

---

## 14. Borg에서 발생한 문제

Borg task는 자동으로 machine 사이를 이동한다.

Replica에는 이 특성이 허용 가능했지만 master에는 문제가 됐다.

당시 master failover는 instance당 약:

```text
30 ~ 90 minutes
```

걸렸다.

Shared machine reboot와 machine failure 때문에 여러 failover가 매주 발생할 수 있었다.

Manual failover 방식으로는:

- 많은 human hours가 필요하고
- best-case availability도 약 99%에 그치며
- error budget을 맞추기 위해 필요한 30초 이하 failover가 불가능했다.

따라서 failover automation이 필요했다.

---

## 15. Decider

2009년 Ads SRE는 automated failover daemon인 **Decider**를 완성했다.

Decider는 planned / unplanned MySQL failover를:

```text
95% of the time
< 30 seconds
```

에 완료할 수 있었다.

이를 통해 MySQL on Borg(MoB)가 가능해졌다.

시스템은 failure를 피하는 방식에서:

> failure는 불가피하므로 automation을 통해 빠르게 복구하는 방식

으로 바뀌었다.

---

## 16. MoB의 결과

Automation을 위해 application은 이전보다 훨씬 많은 failure-handling logic을 가져야 했다.

그러나 결과는 매우 컸다.

MoB 이후:

- mundane operational task 시간이 약 95% 감소
- single database task outage가 사람을 page하지 않음
- schema change도 automation
- Ads Database 전체 operational maintenance 비용 약 95% 감소
- bin-packing으로 hardware 약 60% 절약

Automation으로 절약한 시간이 다시 새로운 automation과 infrastructure 개선에 투자되는 선순환이 만들어졌다.

---

# Soothing the Pain: Applying Automation to Cluster Turnups

## 17. Cluster turnup

초기 Google에서는 새 cluster를 turn up하는 일이 new hire training으로도 사용됐다.

대략적인 단계:

1. datacenter power / cooling 준비
2. core switch 및 backbone 연결
3. 초기 server rack 설치
4. DNS, installer, lock service, storage, computing 설정
5. 나머지 machine 배치
6. user-facing service에 resource 할당

특히 4와 6단계는 매우 복잡했다.

일부 service는 100개가 넘는 subsystem과 dependency를 가지고 있었다.

---

## 18. 잘못된 assumption의 위험

한 Bigtable cluster에서는 latency 때문에 12개 disk 중 첫 번째 logging disk를 사용하지 않도록 설정했다.

1년 뒤 automation이:

> 첫 번째 disk를 사용하지 않는 machine은 storage가 구성되지 않은 machine

이라고 가정했다.

그 결과 machine을 초기화해 Bigtable data를 삭제했다.

Real-time replica가 있어 data를 복구할 수 있었지만, 이 사례는 automation이 implicit "safety" signal에 의존할 때의 위험을 보여준다.

---

# Detecting Inconsistencies with Prodtest

## 19. Configuration inconsistency

Cluster 수가 증가하면서 cluster별 hand-tuned flag와 setting이 늘어났다.

Shell script 기반 automation은 다음을 충분히 확인하지 못했다.

- dependency가 모두 available하고 올바르게 configured됐는가?
- configuration과 package가 다른 deployment와 consistent한가?
- configuration exception이 의도된 것인가?

---

## 20. Prodtest

**Prodtest(Production Test)**는 Python unit test framework를 확장해 실제 production service를 test하는 시스템이었다.

각 team의 Prodtest는 특정 cluster에서 해당 team의 service configuration을 검증했다.

Dependency가 있는 test chain을 구성했고, 앞 단계가 실패하면 이후 test를 중단했다.

이후에는 test state graph도 제공해:

- 어떤 step이 실패했는지
- service가 왜 준비되지 않았는지

쉽게 확인할 수 있었다.

새로운 misconfiguration을 발견하면 Prodtest에 새로운 test를 추가하여 같은 문제가 더 일찍 발견되도록 했다.

---

# Resolving Inconsistencies Idempotently

## 21. Test에서 Fix로

Prodtest는 misconfiguration을 발견할 수 있었지만 직접 수정하지는 못했다.

Google은 각 test에 **fix**를 연결하는 방향으로 발전시켰다.

Fix가 idempotent하다면 15분마다 반복 실행해도 cluster configuration을 손상시키지 않을 수 있다.

Test failure:

```text
Test
↓
Fix
↓
Retry Test
```

형태로 동작했다.

Fix가 여러 번 실패하면 automation을 중단하고 사용자에게 알렸다.

---

## 22. 이 방식의 한계

이 approach로 cluster를 network-ready 상태에서 실제 traffic serving 상태까지 1~2주 내에 만들 수 있었다.

하지만 나중에 보면 문제가 있었다.

- test와 fix 사이 latency
- flaky test
- 모든 fix가 자연스럽게 idempotent하지 않음
- 잘못된 fix가 inconsistent state를 만들 수 있음

---

# The Inclination to Specialize

## 23. Automation process의 세 속성

책에서는 automation process를 세 가지로 평가한다.

- **Competence**: 정확성
- **Latency**: 모든 step이 실행되는 속도
- **Relevance**: 실제 process 중 automation이 포괄하는 비율

Service owner가 직접 automation을 관리할 때는:

- competence 높음
- relevance 높음
- latency 높음

이었다.

Turnup 전담 team을 만들면 latency는 줄었지만 시간이 지나면서 domain expert와 automation operator가 분리됐다.

---

## 24. Specialization의 문제

Real world의 software, configuration, data는 계속 변한다.

Automation을 실제 service owner와 분리하면:

- 새로운 step 누락
- 새로운 flag 때문에 failure
- automation과 service implementation의 불일치

가 발생한다.

책에서는 다음과 같은 잘못된 incentive를 설명한다.

- 현재 turnup 속도만 책임지는 team은 production의 technical debt를 줄일 incentive가 없음
- automation을 직접 실행하지 않는 team은 automation하기 쉬운 system을 만들 incentive가 없음
- automation 품질이 product schedule에 영향을 주지 않으면 product manager는 feature를 우선하게 됨

가장 functional한 tool은 일반적으로 실제 사용하는 사람이 작성한다.

---

## 25. Admin Server

Security requirement 때문에 SSH 기반 automation을 줄여야 했다.

Google은 authenticated, ACL-driven, RPC-based **Local Admin Daemon(Admin Server)**을 도입했다.

이를 통해:

- machine 변경 권한을 세분화
- 모든 operation에 audit trail 생성
- code review 기반 변경
- RPC requestor, parameter, result logging

이 가능해졌다.

---

# Service-Oriented Cluster-Turnup

## 26. Service owner에게 ownership 반환

Admin Server가 service team workflow에 포함되면서 cluster turnup은 SOA 문제로 접근됐다.

각 service owner는 cluster turnup / turndown용 Admin Server를 제공했다.

Turnup automation은 service team의 implementation을 직접 알 필요 없이 해당 API를 호출했다.

즉 각 team은:

```text
Contract / API
```

를 제공하고 내부 implementation은 자유롭게 변경할 수 있었다.

이 방식은:

- low latency
- competent
- accurate

한 turnup process를 만들었고, team과 service 수가 증가해도 유지될 수 있었다.

---

## 27. Cluster turnup automation의 진화

책은 다음과 같이 다시 정리한다.

1. Operator-triggered manual action
2. Operator-written, system-specific automation
3. Externally maintained generic automation
4. Internally maintained, system-specific automation
5. Autonomous systems that need no human intervention

---

# Borg: Birth of the Warehouse-Scale Computer

## 28. 초기 cluster management

초기 Google cluster는 특정 machine에 특정 role을 할당하는 방식이었다.

Engineer는 master machine에 login해 administrative task를 수행했고, golden binary와 configuration도 master에 있었다.

Production이 커지면서 machine 역할을 descriptor file로 관리하고 parallel SSH 형태의 operation을 사용했다.

초기 automation은 Python script 형태로 다음을 처리했다.

- service restart
- 어떤 service가 어떤 machine에서 돌아야 하는지 tracking
- log parsing

---

## 29. Machine-centric abstraction의 한계

Automation은 점점 machine lifecycle을 자동화했지만 abstraction 자체는 physical machine에 묶여 있었다.

이를 벗어나기 위해 **Borg**가 등장했다.

Borg는 cluster를 개별 machine 집합이 아니라:

> managed sea of resources

로 취급했다.

Central coordinator에 API call을 보내 cluster를 관리했고:

- efficiency
- flexibility
- reliability

를 높였다.

Batch task와 user-facing task를 같은 machine에서 scheduling하는 것도 가능해졌다.

---

## 30. Automated에서 Autonomous로

Borg 기반 infrastructure에서는:

- OS upgrade가 지속적으로 자동 수행
- machine state deviation 자동 수정
- broken machine lifecycle 자동 처리
- 매일 수천 대의 machine이 생성·폐기·수리되어도 SRE 개입 불필요

하게 됐다.

초기 automation이 시간을 벌어주었고, 그 시간을 이용해 cluster management 자체를 **autonomous system**으로 바꿀 수 있었다.

---

## 31. Warehouse-scale computer

책에서는 cluster를 하나의 giant computer처럼 바라본다.

다른 machine으로 rescheduling하는 것은 single machine에서 process가 다른 CPU로 이동하는 것과 비슷하다.

Cluster turnup도 새로운 schedulable capacity를 추가하는 것으로 볼 수 있다.

규모가 커질수록 hardware failure는 통계적으로 항상 발생하기 때문에 global computer는 스스로 repair할 수 있어야 한다.

Manual → automatic → autonomous로 갈수록 system에는 **self-introspection** 능력이 필요하다.

---

# Reliability Is the Fundamental Feature

## 32. Automation의 부작용

Automation이 매우 잘 동작하면 human operator가 system과 직접 접촉할 기회가 줄어든다.

결국 automation이 실패했을 때:

- 사람의 실전 대응 능력이 떨어져 있고
- system에 대한 mental model이 현실과 달라져 있을 수 있다.

특히 manual fallback이 항상 가능하다고 가정하는 nonautonomous system에서 문제가 된다.

시간이 지나면 manual operation 자체가 더 이상 가능하지 않을 수도 있다.

---

## 33. Reliability가 핵심

Google에서도 automation이 상황을 악화시킨 사례가 있었다.

그러나 규모가 커질수록 automation과 autonomous behavior는 선택 사항이 아니게 된다.

책의 결론:

> **Reliability is the fundamental feature.**

Autonomous하고 resilient한 behavior는 reliability를 얻는 중요한 방법 중 하나다.

---

# Recommendations

## 34. Design 단계에서 autonomous behavior 고려

Automation은 단순 time saving 이상의 가치가 있기 때문에 Google 규모가 아니더라도 유용하다.

가장 leverage가 큰 시점은 **system design 단계**다.

충분히 커진 시스템에 autonomous operation을 나중에 retrofit하기는 어렵다.

도움이 되는 software engineering practice:

- decoupled subsystem
- API
- side effect 최소화

---

# Automation: Enabling Failure at Scale

## 35. Diskerase 사고

Google은 third-party colocation facility의 rack install/decommission도 크게 자동화했다.

Decommission 과정에는 disk 전체를 지우는 **Diskerase** 단계가 있었다.

어느 날 decommission automation이 Diskerase 완료 후 실패했다.

Debugging을 위해 process를 처음부터 다시 시작하자 automation은:

```text
아직 Diskerase할 machine set = empty
```

라고 판단했다.

문제는 empty set이 특별한 의미로:

```text
everything
```

으로 해석됐다는 점이다.

그 결과 automation은 거의 모든 colo machine을 Diskerase에 보냈다.

---

## 36. 결과

몇 분 안에 CDN machine의 disk가 지워졌다.

Google datacenter 자체 capacity가 충분했기 때문에 외부 사용자는 약간의 latency 증가만 경험했고 대부분 문제를 알아차리지 못했다.

복구에는:

- affected colo machine 재설치 약 2일
- 이후 automation audit
- sanity check 추가
- rate limiting 추가
- decommission workflow idempotent화

가 필요했다.

이 사례는 automation이 **failure도 매우 빠른 속도로 확산시킬 수 있음**을 보여준다.

---

# Chapter 7 핵심 정리

- Automation은 단순 time saving 도구가 아니라 consistency, speed, reliability, scalability를 위한 platform이다.
- Automation 자체가 목표가 아니며, 가능한 경우 외부 automation조차 필요 없는 autonomous system이 더 낫다.
- Automation은 manual → system-specific → generic → internally maintained → autonomous 단계로 진화할 수 있다.
- Automation ownership이 실제 service owner와 분리되면 relevance와 correctness가 떨어질 수 있다.
- Idempotency, API, auditability, ownership이 automation의 중요한 특성이다.
- Borg는 machine-centric operation을 resource-centric autonomous management로 변화시켰다.
- Automation은 failure를 줄일 수도 있지만 잘못 설계하면 failure를 대규모로 확산시킬 수도 있다.
- 궁극적인 목표는 reliability이며, autonomous resilient behavior는 이를 달성하는 중요한 수단이다.
