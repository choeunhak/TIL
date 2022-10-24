
#### Junit4
- All in one


#### Junit5
 - Junit Platform + Junit Jupiter + Junit Vintage


 
|Junit4|Junit5|
|--|--|
|@BeforeClass @AfterClass|@BeforeAll @AfterAll|
|@Before @After|@BeforeEach @AfterEach|
|@Ignore|@Disable|
|@Catefory|@Tag|

각 기능에 대한 설명은 아래 참조링크 참조하면됨.

### Assertions
#### Junit4
- Assert Class
- Optional assertion message 처음 파라미터

#### Junit5
- Assertions class
- Optional assertion message 마지막 파라미터
- assertThat method 없음
- New methods : assertAll, assertThrows



[참조1](https://jade314.tistory.com/entry/Junit-5)