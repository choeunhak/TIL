import java.util.EmptyStackException;

class Stack<T>{
	
	
//	���׸��� ����
//	��� ������ ������Ÿ���� �ٷ���ֵ��� �Ϲ�ȭ�� Ÿ�ԸŰ������� Ŭ������ �޼ҵ带 �ۼ��ϴ� ���
	class Node<T>{
		private T data;
		private Node<T> next;
		public Node(T data) {
			this.data= data;
			
		}
	}
	
	private Node<T> top;
	
	public T pop() {//�Ǹ����� �������鼭 �����
		if(top==null) {//���� ���� �ִ� ��带 ������
			throw new EmptyStackException();//null�̸� �ͼ��ǿ���
		}
		T item = top.data;
		top=top.next;//�״����ּҸ� ž���� �������
		return item;
	}
	
	public void push(T item) {//������ �״°�
		Node<T> t = new Node<T>(item);
		t.next = top;
		top=t;
	}
	
	
	public T peek() {//�������� ���°�
	if(top==null) {//nullüũ
		throw new EmptyStackException();
	}
	return top.data;//ž�� �����͸� ��ȯ
	}
	
	public boolean isEmpty() {//������ ����� Ȯ���ϴ°�
		return top==null;
	}
	
}


public class StackTest {

	public static void main(String[] args) {
		//������ ����� �״�,, �ù�, last in first out 
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
