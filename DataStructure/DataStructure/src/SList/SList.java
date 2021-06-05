package SList;
import java.util.NoSuchElementException;


public class SList <E extends Comparable<E>>{
	
	protected Node head;//연결리스트의 첫노드
	private int size;
	
	public SList() {
		head = null;
		size = 0;
	}
	
	
	public int size() { return size;}
	public boolean isEmpty() { return size==0; }
	
	public int search(E target) {//찾기
		Node p = head;
		
		for(int k=0; k<size; k++) {
			if(target == p.getItem()) {
				return k;
			}
			p=p.getNext();
		}
		return -1;
	}
	
	public void insertFront(E newItem) {//새노드를 첫번째노드가 되도록 연결
		head = new Node(newItem,head);//어떻게 다음노드를 찾기? 다음노드 연결안시키고... 아 기존의 head를 주는구나...
		size++;
	}
	
	public void insertAfter(E newItem, Node p) {//p노드 다음에 삽입
		p.setNext(new Node(newItem, p.getNext()));
		size++;
	}
	
	public void deleteFront() {
		if(isEmpty()) throw new NoSuchElementException();
		head = head.getNext();//그냥 원래 헤드신경안쓰고 헤드다음거를 헤드로 연결시켜버림
		size--;
		
	}
	
	public void deleteAfter(Node p) {//p가 가리키는 노드의 다음 노드를 삭제...
		if(p==null) throw new NoSuchElementException();
		
		Node t = p.getNext();//원래 p가 가리키고 있던 다음 노드 저장
		p.setNext(t.getNext());//차근차근이해해라..
		t.setNext(null);
		size--;
	}
	
	public void print() {
		for (Node p =head; p!=null; p=p.getNext()){
			System.out.print(p.getItem()+"  ");
		}
		System.out.println();
	}
	

	public SList merge(Node n1, Node n2) {
		
		Node last = this.head;
		
		while(n1!=null && n2!=null) {
			if(n1.getItem().compareTo(n2.getItem())<0) {//n2가큼
				last.setNext(n1);
				n1=n1.getNext();
		}
			else {
				last.setNext(n2);
				n2=n2.getNext();
			}
			last=last.getNext();
		}
		if(n1==null) {
			last.setNext(n2);
		}
		else if(n2==null) {
			last.setNext(n1);
		}
		this.deleteFront();
		return this;
	}
	
	public void split(int k, SList s5, SList s6) {
		Node n4 = this.head;
		while(n4!=null) {
			if(n4.getItem().compareTo(k)>0) {//9,8
				s5.insertFront(n4.getItem());
			}
			else {//2476
				s6.insertFront(n4.getItem());
			}
			n4=n4.getNext();
		}
	}
	

	


}
