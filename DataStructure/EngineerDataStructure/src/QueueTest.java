import java.util.NoSuchElementException;

class Queue<T>{
	
	class Node<T>{
		private T data;
		private Node<T> next;
		
		public Node(T data) {//������
			this.data=data;
		}
	}
	
	private Node<T> first;//�յڷ� �ּҸ� �˰��־����(������ top�� �ּҸ� �˰��־���)
	private Node<T> last;
	
	
	public void add(T item) {
		Node<T> t = new Node<T>(item);
		
		if(last!=null) {//��Ʈ ��尡 ������
			last.next=t;//�� �ڿ� ���� ������ ��带����
		}
		last=t;//t�� ���� ������ ���
		if(first==null) {//�����Ͱ� ����������
			first=last;//���� ���� �Ҵ�����
		}
	}
	
	public T remove() {
		if(first==null) {//ť�� ��������� ����
			throw new NoSuchElementException();
		}
		//�״����� �ּҸ� �������� �������
		T data = first.data;//�����͸� ����ϴ´ܰ�
		first = first.next;//�����ָ� first�� �������
		if(first==null) {//first�� null�̸� last��null�� ����
			last=null;
		}
		return data;
	}
	
	public T peek() {
		if(first==null) {
			throw new NoSuchElementException();
		}
		return first.data;//null�̾ƴϸ� first�����͸� ��ȯ
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
