package ListStack;
import java.util.EmptyStackException;


public class ListStack <E>{
	
	protected Node top;
	private int size;
	
	public ListStack() {
		top = null;//top항목을 가진 노드
		size = 0;
	}
	public E peek() {
		if(isEmpty()) {
			throw new EmptyStackException();
		}
		return (E) top.getItem();}
	public int size() { return size;}
	public boolean isEmpty() { return size==0; }
	
	public void push(E newItem) {
		Node newNode = new Node(newItem, top);//top에서 아래를 다음노드로 연결시킴
		top = newNode;
		size++;
	}
	public E pop() {
		if(isEmpty()) throw new EmptyStackException();
		
		E topItem = (E) top.getItem();
		top=top.getNext();
		size--;
		return topItem;
	}
	public void print() {
		for (Node p =top; p!=null; p=p.getNext()){
			System.out.print(p.getItem()+"  ");
		}
		System.out.println();
	}
}
