- ALB, NLB
  - ALB (Application!)
     - OSI 7계층 레벨에서 동작
     - HTTP 및 HTTPS 트래픽을 분산시키는 데 주로 사용됨
     - ALB는 트래픽을 기반으로 한 여러 가용 영역에 있는 EC2 인스턴스, 컨테이너, Lambda 함수 등으로 분배할 수 있습니다. 또한 ALB는 도메인 기반 라우팅, SSL/TLS 종료, 웹 애플리케이션 방화벽 등의 고급 기능을 제공

  - NLB (Network!)
    - NLB는 OSI 4계층(Transport Layer)에서 동작
    - TCP, UDP 및 TLS 트래픽을 분산시키는 데 사용
    - NLB는 빠른 성능, 고가용성, 정적 IP 주소를 제공하여 애플리케이션의 네트워크 수준에서의 로드 밸런싱을 처리
    - NLB는 클라이언트 IP 기반 세션 지속성, 대기 시간 기반 라우팅 등의 고급 기능을 지원

- 하지만, AWS ALB(Application Load Balancer)는 고정 IP 주소(탄력적 IP 또는 EIP)를 직접적으로 지원하지 않음
- ALB는 동적으로 IP 주소를 할당받고, 이는 해당 ALB의 수명 주기 동안 유지됨 따라서 특정 클라이언트의 요청이 항상 동일한 IP 주소로 전달되지 않을 수 있다.
- AWS NLB(Network Load Balancer)는 EIP(Elastic IP)를 사용할 수 있는 로드 밸런서
- NLB는 고정 IP 주소를 제공하며, 이를 통해 클라이언트의 요청이 항상 동일한 IP 주소로 전달됨
- NLB는 주로 고정 IP 주소가 필요한 시나리오에서 사용되며, 예를 들어 보안 정책, 네트워크 환경 또는 특정 클라이언트에서 IP 주소를 Whitelist로 필요로 할 때 유용
