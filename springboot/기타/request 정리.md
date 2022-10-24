- **@PathVariable**
    - URL경로에 값를 넣는다 
    - /{값}
    - RestAPI에 주로사용한다


- **@RequstParam**
    - URL파라미터로 값을 넘긴다 
    - /?변수={값}

- **@requestBody**
    - json 형태의 body 내용을 java object로 변환
    - 메시지 컨버터로 MappingJackson2HttpMessageConverter를 활용하여 자바 객체로 변환됨

- **@ModelAttribute**
     - multipart/form-data 형태의 body 내용을 바인딩
     - setter 필요

- [참고자료](https://mangkyu.tistory.com/72)