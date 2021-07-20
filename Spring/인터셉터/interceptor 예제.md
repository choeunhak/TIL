#### 환경설정
spring-servlet.xml

```xml
<!-- Interceptors -->

<mvc:interceptors>
         <mvc:interceptor>
                  <mvc:mapping path="/**" /> 
                  <bean class="com.example.interceptor.Interceptor" />
         </mvc:interceptor>
</mvc:interceptors>
```

##### 구현하는 두가지 방법
- HandlerInterceptor 인터페이스를 구현
- HandlerInterceptorAdapter 클래스를 상속


1. HandlerInterceptor 인터페이스를 구현

preHandle() , postHandle() , afterCompletion() 메서드를 구현해야 함


```java
public class MyInterceptor implements HandlerInterceptor{
	// controller가 호출되기 전 실행
	// 반환이 false라면 controller로 요청을 안함
	// 매개변수 Object는 핸들러 정보를 의미한다. ( RequestMapping , DefaultServletHandler ) 
	@Override
	public boolean preHandle(
			HttpServletRequest request, HttpServletResponse response,
			Object obj) throws Exception {
		
		System.out.println("MyInterCeptor - preHandle");
		return false;
	}

	// controller의 handler가 끝나면 처리(컨트롤러가 실행 된 후 호출)
	@Override
	public void postHandle(
			HttpServletRequest request, HttpServletResponse response,
			Object obj, ModelAndView mav)
			throws Exception {
	}

	// view까지 처리가 끝난 후에 처리
	@Override
	public void afterCompletion(
			HttpServletRequest request, HttpServletResponse response,
			Object obj, Exception e)
			throws Exception {
	}
}
```


2. HandlerInterceptorAdapter 클래스를 상속 받아 구현
- 이미 postHandle() , afterCompletion() 가 구현되어 있어 오바리이딩해서 사용


실제 사용 예시
- 로그인 처리

### *왜 로그인 처리에 이용하냐????*
- [악덕 고용주의 개발일기 인용](https://rongscodinghistory.tistory.com/2)

만약 인터셉터를 이용하지 않고, 로그인 처리를 한다면, 게시물을 작성("/board/register"), 게시물 수정("/board/modify"),

 게시물 삭제("/board/delete") 등 모든 요청마다 Controller에서 session을 통해 로그인 정보가 남아 있는지를 확인하는 코드

 를 중복해서 입력해야 할 것이다. 

 하지만!, 인터셉터를 이용하면, A, B, C 작업(A,B,C 경로로 요청)을 할 경우에는 ~~Interceptor를 먼저 수행해 session에서 

 로그인 정보가 있는지 확인해 주는 역할을 한다면, 중복 코드가 확 줄어들 수 있을 것이다. 이러한 장점 때문에 사용!







- [인터셉터 유튜브 강의 참조](https://www.youtube.com/watch?v=6rNZFo4eyhE)
- [빅토리 블로그 참조](https://victorydntmd.tistory.com/176)