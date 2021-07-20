import java.util.EmptyStackException;

class Stack<T>{
	
	
//	제네릭의 개념
//	모든 종류의 데이터타입을 다룰수있도록 일반화된 타입매개변수로 클래스나 메소드를 작성하는 기법
	class Node<T>{
		private T data;
		private Node<T> next;
		public Node(T data) {
			this.data= data;
			
		}
	}
	
	private Node<T> top;
	
	public T pop() {//맨마지막 가져오면서 지우기
		if(top==null) {//가장 위에 있는 노드를 가져옴
			throw new EmptyStackException();//null이면 익셉션에러
		}
		T item = top.data;
		top=top.next;//그다음주소를 탑으로 만들어줌
		return item;
	}
	
	public void push(T item) {//맨위에 쌓는거
		Node<T> t = new Node<T>(item);
		t.next = top;
		top=t;
	}
	
	
	public T peek() {//맨위에거 보는거
	if(top==null) {//null체크
		throw new EmptyStackException();
	}
	return top.data;//탑의 데이터를 반환
	}
	
	public boolean isEmpty() {//스택이 비었나 확인하는것
		return top==null;
	}
	
}


public class StackTest {

	public static void main(String[] args) {
		//스택은 영어로 쌓다,, 택배, last in first out 
		Stack<Integer> s = new Stack<Integer>();
		s.push(1);
		s.push(2);
		s.push(3);
		s.push(4);
		System.out.println(s.pop());
		System.out.println(s.pop());
		System.out.println(s.peek());
		System.out.println(s.pop());
		System.out.println(s.isEmpty());
	}

}
