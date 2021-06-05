package HashTest;

class QuadProbing<K, V>{
	  private int N = 0, M = 10;
	  private K[] a = (K[]) new Object[M]; // 해시테이블
	  private V[] d = (V[]) new Object[M]; // key관련 데이터 저장
	  // 해시코드
	  private int hash(K Key){
	    return (Key.hashCode() & 0x7fffffff) % M; // 나눗셈 함수
	  }
	  // 삽입 연산
	  public void put(K key, V data){
	    int initialpos = hash(key); // 초기 위치
	    int i = initialpos, j = 1;
	    do{
	      if (a[i] == null){ // 삽입 위치 발견
	        a[i] = key; // key를 해시테이블에 저장
	        d[i] = data; N++; // key관련 데이터 저장, 항목 수 1증가
	        return;
	      }
	      if (a[i].equals(key)){ // 이미 key 존재
	        d[i] = data; // data만 갱신
	        return;
	      }
	      i = (initialpos + j * j++) % M; // i = 다음 위치
	    } while(N < M);
	  }
	  // 탐색 연산
	  public V get(K key){
	    int initialpos = hash(key);
	    int i = initialpos, j = 1;
	    while (a[i] != null){ // a[i]가 empty가 아니면
	      if (a[i].equals(key))
	        return d[i]; // 탐색 성공
	      i = (initialpos + j * j++) % M; // i = 다음 위치  
	    }
	    return null; // 탐색 실패
	  }
	  // 해시 테이블 보기
	  public void print(){
		    for (int i = 0; i < M; i++){
		      System.out.print(i + "	");
		    }
		    System.out.println();
		    for (int i = 0; i < M; i++){
			  System.out.print(a[i] + "	");
		}
		    System.out.println();
		  }
	}