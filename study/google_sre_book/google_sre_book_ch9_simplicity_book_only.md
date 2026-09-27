# Google SRE Book — Chapter 9: Simplicity

원문: https://sre.google/sre-book/simplicity/

---

## 1. 핵심 메시지

Software system은 본질적으로 dynamic하고 unstable하다.

완전히 stable하려면:

- code가 바뀌지 않고
- hardware나 library가 바뀌지 않고
- user 수가 증가하지 않아야 한다.

현실적인 production system에서는 불가능하다.

SRE의 핵심 과제는:

> **agility와 stability 사이의 균형을 유지하는 것**

이다.

---

# System Stability Versus Agility

## 2. Stability와 agility

상황에 따라 agility를 위해 stability를 희생하는 것이 합리적일 수 있다.

책에서는 unfamiliar problem domain을 이해하기 위한 **exploratory coding**을 예로 든다.

이런 code는 explicit shelf life를 가지고 production에 배포하지 않을 예정이므로 test coverage와 release management를 느슨하게 할 수 있다.

---

## 3. Production system의 균형

대부분의 production software는 stability와 agility를 함께 필요로 한다.

SRE는:

- procedure
- practice
- tool

을 통해 software reliability를 높이면서 developer agility에 미치는 영향을 최소화한다.

Reliable process는 오히려 developer agility를 높일 수도 있다.

빠르고 reliable한 production rollout은 change의 영향을 쉽게 확인하게 하고, bug를 더 빨리 찾아 수정할 수 있게 한다.

---

# The Virtue of Boring

## 4. Boring software

Software에서 **boring**은 좋은 특성이다.

Program은 surprise를 만들기보다 예측 가능한 방식으로 business goal을 수행해야 한다.

Production surprise는 SRE가 피해야 할 대상이다.

---

## 5. Essential complexity vs Accidental complexity

Fred Brooks의 구분을 사용한다.

### Essential complexity

문제 자체에 본질적으로 포함되어 제거할 수 없는 complexity.

예:

- web server가 page를 빠르게 serve해야 하는 문제

### Accidental complexity

구현 방식 때문에 생겨 engineering effort로 제거할 수 있는 complexity.

예:

- Java web server에서 garbage collection performance impact를 줄이기 위한 complexity

SRE team은:

- accidental complexity가 추가될 때 push back하고
- onboarding한 system의 unnecessary complexity를 지속적으로 제거해야 한다.

---

# I Won’t Give Up My Code!

## 6. Dead code를 남겨두지 않는다

Engineer는 자신이 만든 code에 감정적으로 attachment를 가질 수 있다.

다음과 같은 이유로 code deletion을 피하려 할 수 있다.

- 나중에 필요할 수 있다
- comment 처리해 두자
- flag 뒤에 숨겨 두자

책은 이런 방식을 좋지 않다고 본다.

Source control이 있으므로 필요하면 과거 code를 복원할 수 있다.

반면:

- 대량의 commented-out code는 confusion을 만들고
- 항상 disabled된 flag 뒤 code는 future failure source가 될 수 있다.

Knight Capital 사례가 이러한 위험의 예로 언급된다.

---

## 7. 모든 code는 liability가 될 수 있다

24/7 availability가 필요한 service에서는 모든 새로운 line of code가 일정 부분 liability가 될 수 있다.

SRE는 다음 practice를 권장한다.

- code가 실제 business goal에 필요한지 검토
- dead code를 지속적으로 제거
- testing 단계에 bloat detection 포함

---

# The "Negative Lines of Code" Metric

## 8. Software bloat

Software는 feature가 계속 추가되면서 점점:

- 커지고
- 느려지고

복잡해질 수 있다.

SRE 관점에서 모든 code addition/change는 새로운 defect와 bug의 가능성을 만든다.

작은 project는 일반적으로:

- 이해하기 쉽고
- test하기 쉽고
- defect가 적다.

따라서 새로운 feature를 추가하는 것만큼 불필요한 code를 삭제하는 것도 가치가 있다.

---

# Minimal APIs

## 9. API는 작고 단순하게

Minimal API는 software simplicity의 핵심이다.

Method와 argument가 적을수록:

- API를 이해하기 쉽고
- 각 method의 품질에 더 집중할 수 있다.

모든 문제를 해결하려 하기보다 어떤 문제는 명시적으로 해결하지 않기로 결정하면 core problem에 더 집중할 수 있다.

작고 단순한 API는 문제 자체가 잘 이해됐다는 신호이기도 하다.

---

# Modularity

## 10. Loose coupling

Distributed system에도 object-oriented design의 많은 원칙을 적용할 수 있다.

System 일부를 독립적으로 변경할 수 있어야 supportable system을 만들 수 있다.

특히:

- binary 사이
- binary와 configuration 사이

의 **loose coupling**은 developer agility와 system stability를 동시에 높인다.

---

## 11. 독립적인 변경

큰 system의 일부 program에 bug가 생기면 전체 system을 변경하지 않고 해당 component만 수정해 production에 push할 수 있어야 한다.

이러한 isolation이 modularity의 중요한 가치다.

---

## 12. API versioning

API change 하나가 전체 system rebuild를 요구하면 새로운 bug risk도 커진다.

API를 versioning하면 기존 consumer는 필요한 version을 계속 사용하면서 안전하게 새로운 version으로 이동할 수 있다.

System 전체가 동일한 release cadence를 가질 필요가 없고 component별로 다른 cadence를 가질 수 있다.

---

## 13. Responsibility separation

System이 복잡해질수록 API와 binary 사이 responsibility 분리가 더 중요해진다.

Object-oriented class에서 unrelated function을 한 class에 넣는 것이 좋지 않은 것처럼 distributed system에서도:

- `util`
- `misc`

형태로 unrelated responsibility를 한 binary에 넣는 것은 좋지 않다.

Well-designed distributed system의 각 component는 명확하고 제한된 purpose를 가져야 한다.

---

## 14. Data format의 modularity

Modularity는 data format에도 적용된다.

Google Protocol Buffers의 중요한 design goal 중 하나는:

- backward compatibility
- forward compatibility

를 제공하는 wire format을 만드는 것이다.

---

# Release Simplicity

## 15. 작은 release

Simple release는 complicated release보다 좋다.

한 번에 하나의 change를 release하면 impact를 측정하고 이해하기 쉽다.

반대로 unrelated change 100개를 한 번에 release한 뒤 performance가 나빠지면 어느 change가 원인인지 확인하기 어렵다.

---

## 16. Small batch의 장점

Release를 작은 batch로 수행하면 각 code change를 isolation된 상태로 이해할 수 있기 때문에 더 빠르고 자신 있게 움직일 수 있다.

책에서는 이를 machine learning의 **gradient descent**에 비유한다.

작은 step을 하나씩 적용하면서:

- improvement인지
- degradation인지

확인하는 방식이다.

---

# A Simple Conclusion

## 17. Simplicity와 reliability

Chapter의 반복되는 핵심은:

> **software simplicity is a prerequisite to reliability**

이다.

Task를 단순화하는 것은 게으름이 아니다.

실제로 달성하려는 목적이 무엇인지 명확하게 하고, 가장 단순한 방법으로 그 목적을 달성하려는 것이다.

---

## 18. "No"의 가치

Feature에 "no"라고 하는 것은 innovation을 막는 것이 아니다.

불필요한 distraction을 system에서 제거하여 실제 innovation과 engineering에 집중할 공간을 유지하는 것이다.

---

# Chapter 9 핵심 정리

- Production software는 stability와 agility 사이의 균형이 필요하다.
- Reliable process는 developer agility를 낮추는 것이 아니라 오히려 높일 수 있다.
- Production software는 예측 가능하고 boring할수록 좋다.
- Essential complexity는 받아들여야 하지만 accidental complexity는 제거해야 한다.
- Dead code와 불필요한 code는 reliability liability이므로 적극적으로 삭제한다.
- 작은 codebase는 이해, testing, defect 관리가 쉽다.
- API는 가능한 한 minimal해야 한다.
- Modularity와 loose coupling은 system stability와 developer agility를 동시에 높인다.
- API와 data format의 compatibility는 component를 독립적으로 변화시킬 수 있게 한다.
- Release는 작은 batch로 수행할수록 impact를 이해하기 쉽다.
- Software simplicity는 reliability의 전제 조건이다.
