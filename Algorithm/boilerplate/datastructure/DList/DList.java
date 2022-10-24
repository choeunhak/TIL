package DList;
import java.util.NoSuchElementException;


public class DList <E extends Comparable<E>>{
	
	protected DNode head, tail;
	protected int size;
	
	public DList() {
		head = new DNode(null, null, null);
		tail = new DNode(null, head, null);//head노드를 이전노드로 설정
		head.setNext(tail);//tail노드를 다음노드로 설정
		size = 0;
	}
	public void insertBefore(DNode p, E newItem) {//p가 가리키는 노드 앞에 삽입
		DNode t = p.getPrevious();//그냥 p 이전노드만 찾고 
		DNode newNode = new DNode(newItem, t,p);//t랑 p 연결시켜버림
		p.setPrevious(newNode);
		t.setNext(newNode);
		size++;
	}
	public void insertAfter(DNode p, E newItem) {
		DNode t = p.getNext();
		DNode newNode = new DNode(newItem, p,t);
		t.setPrevious(newNode);
		p.setNext(newNode);
		size++;
	}
	public void delete(DNode x) {
		if(x==null) throw new NoSuchElementException();
		
		DNode f =x.getPrevious();
		DNode r =x.getNext();
		f.setNext(r);
		r.setPrevious(f);
		size--;
	}
	public void print() {
		if(size>0) {
		for (DNode p =head.getNext(); p!=tail; p=p.getNext()){
			System.out.print(p.getItem()+"  ");
		}
		}
		else {
			System.out.println("리스트 비어있음");
		}
		System.out.println();
	}

}
