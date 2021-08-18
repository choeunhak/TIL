- /login은 기본적으로 security에서 낚아챈다
- securityconfig를 생성한 후에는 작동 안한다
- 권한 설정->securityconfig
    - role
    - .loginPage("/login")으로 하면 권한 없을 때 여기로 이동
![](images/2021-08-18-17-06-12.png)
- csrf 설정...