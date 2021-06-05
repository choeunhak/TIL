import java.util.NoSuchElementException;

class Queue<T>{
	
	class Node<T>{
		private T data;
		private Node<T> next;
		
		public Node(T data) {//생성자
			this.data=data;
		}
	}
	
	private Node<T> first;//앞뒤로 주소를 알고있어야함(스택은 top의 주소만 알고있었다)
	private Node<T> last;
	
	
	public void add(T item) {
		Node<T> t = new Node<T>(item);
		
		if(last!=null) {//라스트 노드가 있으면
			last.next=t;//그 뒤에 새로 생성한 노드를붙임
		}
		last=t;//t가 이제 마지막 노드
		if(first==null) {//데이터가 없을때에는
			first=last;//같은 값을 할당해줌
		}
	}
	
	public T remove() {
		if(first==null) {//큐가 비어있으면 에러
			throw new NoSuchElementException();
		}
		//그다음의 주소를 다음으로 만들어줌
		T data = first.data;//데이터를 백업하는단계
		first = first.next;//다음애를 first로 만들어줌
		if(first==null) {//first가 null이면 last도null로 변경
			last=null;
		}
		return data;
	}
	
	public T peek() {
		if(first==null) {
			throw new NoSuchElementException();
		}
		return first.data;//null이아니면 first데이터를 반환
	}
	
	public boolean isEmpty() {
		return first == null;
	}
}


public class QueueTest {//FIFO

	public static void main(String[] args) {
		Queue<Integer> q =new Queue<Integer>();
		q.add(1);
		q.add(2);
		q.add(3);
		q.add(4);
		System.out.println(q.remove());
		System.out.println(q.remove());
		System.out.println(q.peek());
		System.out.println(q.remove());
		System.out.println(q.isEmpty());
	}

}
