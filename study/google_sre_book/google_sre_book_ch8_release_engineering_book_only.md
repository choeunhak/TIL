# Google SRE Book — Chapter 8: Release Engineering

원문: https://sre.google/sre-book/release-engineering/

---

## 1. Release Engineering

Release engineering은 software를 **build하고 deliver하는 과정**을 다루는 software engineering discipline이다.

Release engineer는 다음 영역을 이해한다.

- source code management
- compiler
- build configuration language
- automated build tool
- package manager
- installer
- development
- configuration management
- test integration
- system administration
- customer support

Reliable service에는 reliable release process가 필요하다.

SRE는 binary와 configuration이:

- reproducible
- automated
- repeatable

한 방식으로 만들어졌다는 것을 신뢰할 수 있어야 한다.

Release process의 변화는 accidental하지 않고 intentional해야 한다.

---

# The Role of a Release Engineer

## 2. Release engineer의 역할

Google에서 release engineering은 독립적인 직무다.

Release engineer는 SWE와 SRE와 함께 source code에서 deployment까지 release에 필요한 전체 step을 정의한다.

예:

- source code repository 관리 방식
- compilation build rule
- testing
- packaging
- deployment

---

## 3. Data-driven release engineering

Google은 release engineering에서도 metric을 사용한다.

예:

- code change가 production에 배포되기까지 걸리는 시간
- build configuration에서 어떤 feature가 사용되는지

Release engineer는 release process의 best practice와 tool을 만든다.

---

## 4. SRE와의 협업

Release engineer와 SRE는 다음 전략을 함께 만든다.

- change canarying
- service interruption 없는 rollout
- 문제가 발생한 feature rollback

---

# Philosophy

Google release engineering은 네 가지 principle을 따른다.

---

## 5. Self-Service Model

Scale하기 위해 team은 자신의 release process를 직접 운영할 수 있어야 한다.

Release engineering은 product team이 스스로 release를 control하고 실행할 수 있는 tool과 best practice를 제공한다.

개별 team은:

- 언제 release할지
- 얼마나 자주 release할지

결정할 수 있다.

많은 project는 automated build와 deployment tool을 통해 engineer 개입 없이 build/release된다.

사람은 문제가 발생할 때만 개입한다.

---

## 6. High Velocity

User-facing software는 자주 rebuild된다.

Google은 frequent release를 통해 version 사이 change 수를 줄이는 방식을 선호한다.

Change가 작으면:

- testing이 쉬워지고
- troubleshooting이 쉬워진다.

일부 team은 hourly build를 수행하고 test result와 포함된 feature를 기준으로 production version을 선택한다.

다른 team은 **Push on Green** 방식을 사용해 모든 test를 통과한 build를 자동 배포한다.

---

## 7. Hermetic Builds

동일한 source revision을 다른 machine에서 build하더라도 동일한 결과가 나와야 한다.

Hermetic build는 build machine에 설치된 library나 software에 영향을 받지 않는다.

대신 명시된 version의:

- compiler
- build tool
- dependency

를 사용한다.

Build process는 self-contained해야 하며 build environment 외부 service에 의존하지 않는다.

---

## 8. Older release rebuild와 cherry picking

Production에 있는 과거 release에 bug fix가 필요할 수 있다.

Google은 원래 release와 같은 revision에서 다시 build하고 필요한 새로운 change만 포함한다.

이를 **cherry picking**이라고 한다.

Build tool 자체도 source repository revision에 따라 versioning되므로 과거 release를 다시 build할 때 당시 compiler/tool version을 사용할 수 있다.

---

## 9. Enforcement of Policies and Procedures

Release 과정의 주요 operation은 access control과 security policy로 보호된다.

Gated operation 예:

- source code change approval
- release process action 지정
- new release 생성
- initial integration proposal 승인
- cherry pick 승인
- release deployment
- build configuration 변경

대부분의 code change는 code review를 필요로 한다.

Automated release system은 release에 포함된 모든 change report를 생성하고 build artifact와 함께 archive한다.

이는 release 문제 troubleshooting에 도움을 준다.

---

# Continuous Build and Deployment

## 10. Rapid

Google은 automated release system **Rapid**를 사용한다.

Rapid는 scalable, hermetic, reliable release를 제공하는 framework다.

---

# Building

## 11. Blaze

Google의 build tool은 **Blaze**다.

Blaze는 다음 언어의 binary를 build할 수 있다.

- C++
- Java
- Python
- Go
- JavaScript

Engineer는 build target과 dependency를 정의하며 Blaze는 dependency target을 자동으로 build한다.

Rapid project configuration에는:

- binary build target
- unit test target

이 정의된다.

Binary에는 다음 정보를 표시하는 flag가 있다.

- build date
- revision number
- build identifier

이를 통해 binary가 어떻게 build됐는지 추적할 수 있다.

---

# Branching

## 12. Mainline과 release branch

모든 code는 main branch(mainline)에 check-in된다.

하지만 대부분의 major project는 mainline에서 직접 release하지 않는다.

특정 revision에서 branch를 만들고 release한다.

Bug fix는 먼저 mainline에 제출한 뒤 release branch로 cherry pick한다.

Branch의 change를 mainline으로 다시 merge하지 않는다.

이 방식으로 각 release의 정확한 contents를 알 수 있다.

---

# Testing

## 13. Continuous testing

Code가 mainline에 submit될 때마다 continuous test system이 unit test를 실행한다.

이를 통해 build/test failure를 빠르게 발견한다.

Release engineering은:

- continuous build에서 실행되는 test와
- 실제 release를 gate하는 test

를 동일하게 맞추는 것을 권장한다.

Release는 마지막으로 모든 continuous test를 성공한 revision에서 만드는 것을 권장한다.

---

## 14. Release branch testing

Release 과정에서는 release branch를 대상으로 unit test를 다시 실행한다.

Cherry pick이 포함되면 release branch의 code version은 mainline 어디에도 존재하지 않을 수 있기 때문이다.

실제로 release할 code가 test를 통과했다는 audit trail을 남긴다.

별도의 testing environment에서는 packaged build artifact를 대상으로 system-level test도 수행한다.

---

# Packaging

## 15. Midas Package Manager

Google은 software distribution에 **Midas Package Manager(MPM)**를 사용한다.

MPM package에는:

- build artifact
- owner
- permission

정보가 포함된다.

Package는:

- 이름
- unique hash version
- signature

를 가지며 authenticity를 보장한다.

---

## 16. Package label

MPM package에는 label을 붙일 수 있다.

예:

- `dev`
- `canary`
- `production`

Rapid는 build ID를 package label로 사용하여 package를 고유하게 reference할 수 있다.

기존 label을 새 package에 붙이면 label은 자동으로 이전 package에서 새 package로 이동한다.

---

# Rapid

## 17. Blueprint와 workflow

Rapid project는 **blueprint**라는 configuration file로 정의한다.

Blueprint에는:

- build target
- test target
- deployment rule
- project owner

등이 들어 있다.

Role-based ACL이 Rapid project에서 누가 어떤 action을 수행할 수 있는지 결정한다.

Workflow는 release 과정의 action을 정의한다.

Action은:

- serial
- parallel

로 실행할 수 있고 다른 workflow를 실행할 수도 있다.

Rapid는 Google production infrastructure 위에서 동작하기 때문에 동시에 수천 개 release request를 처리할 수 있다.

---

## 18. Typical Rapid release process

1. Requested integration revision에서 release branch 생성
2. Blaze로 binary compile 및 unit test 실행
3. Build artifact를 system testing과 canary deployment에 사용
4. 각 step 결과를 log하고 이전 release 이후 모든 change report 생성

Rapid는 release branch와 cherry pick도 관리하며 individual cherry pick request를 승인 또는 거부할 수 있다.

---

# Deployment

## 19. Rapid deployment

단순 deployment에서는 Rapid가 blueprint의 deployment definition에 따라 Borg job이 새 MPM package를 사용하도록 update한다.

---

## 20. Sisyphus

복잡한 rollout에는 SRE가 개발한 general-purpose rollout automation framework인 **Sisyphus**를 사용한다.

Rollout은 여러 task로 구성된 logical unit이다.

Sisyphus는 Python class를 확장하여 다양한 deployment process를 지원할 수 있다.

Dashboard를 통해 rollout 진행 상황을 제어하고 관찰한다.

---

## 21. Service risk에 따른 rollout

Deployment process는 service의 risk profile에 맞춘다.

예:

### Development / pre-production

- hourly build
- test 통과 시 자동 push

### Large user-facing service

- 한 cluster에서 시작
- 이후 exponentially 확장

### Sensitive infrastructure

- 여러 날에 걸쳐 rollout
- geographic region의 instance 사이에 deployment를 분산

---

# Configuration Management

## 22. Configuration도 release 문제다

Configuration change도 instability의 원인이 될 수 있다.

Google은 모든 configuration management 방식에서:

- primary source repository에 configuration 저장
- strict code review

를 요구한다.

---

## 23. Mainline configuration

Configuration을 mainline의 head에서 직접 수정한다.

Review 후 running system에 적용한다.

장점:

- binary release와 configuration change 분리

문제:

- repository configuration과 실제 running configuration 사이 skew 가능

---

## 24. Binary와 configuration을 같은 package에 포함

Configuration file이 적거나 release마다 configuration이 같이 변경되는 project에서는 binary와 configuration을 같은 MPM package에 넣는다.

장점:

- deployment 단순

단점:

- binary와 configuration이 강하게 결합돼 flexibility 감소

---

## 25. Configuration package 분리

Configuration도 hermetic principle을 적용해 별도 MPM configuration package로 만들 수 있다.

Binary와 configuration 각각 package를 만들면:

- version을 함께 추적할 수 있고
- 필요하면 configuration만 새로 build/deploy할 수 있다.

Build ID를 이용해 특정 시점의 configuration을 재구성할 수 있다.

MPM label을 이용해 어떤 binary package와 configuration package가 함께 사용돼야 하는지도 표시할 수 있다.

---

## 26. External store

자주 또는 runtime에 동적으로 변경돼야 하는 configuration은 다음에 저장할 수 있다.

- Chubby
- Bigtable
- source-based filesystem

Project owner는 각 configuration distribution 방식 중 자신의 project에 적합한 것을 선택한다.

---

# Conclusions

## 27. Release engineering의 목표

올바른 tool, automation, policy가 있으면 developer와 SRE는 software release 자체를 걱정하지 않아도 된다.

Release는 가능한 한:

> button을 누르는 것처럼 간단한 과정

이 되어야 한다.

---

# Chapter 8 핵심 정리

- Reliable service에는 reproducible하고 repeatable한 release process가 필요하다.
- Release engineering은 source code에서 production deployment까지 전체 software delivery lifecycle을 다룬다.
- 핵심 철학은 Self-Service, High Velocity, Hermetic Builds, Policy Enforcement다.
- Frequent release는 version당 change 수를 줄여 testing과 troubleshooting을 쉽게 한다.
- Hermetic build는 같은 source revision에서 항상 동일한 build 결과를 만들도록 한다.
- Mainline, release branch, cherry pick을 통해 release content를 정확히 관리한다.
- Continuous testing과 release branch testing으로 실제 release artifact를 검증한다.
- Rapid, Blaze, MPM, Sisyphus가 build/package/deployment lifecycle을 구성한다.
- Deployment 속도와 방식은 service risk profile에 맞춰야 한다.
- Configuration도 code와 마찬가지로 versioning, review, reproducibility가 필요하다.
