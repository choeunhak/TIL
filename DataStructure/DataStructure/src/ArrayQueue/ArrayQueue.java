package ArrayQueue;
import java.util.NoSuchElementException;

public class ArrayQueue<E> {
	private E q[];
	private int front, rear, size;//첫번째노드와 마지막 노드, front에서는 삭제만 이루어지고 rear에서는 삽입만 일어난다
	
	public ArrayQueue() {
		q=(E[]) new Object[2];
		front = rear = size=0;//빈상태만들기위해 -1로 초기화
		}
	
	public int size() {
		return size;
	}
	
	public boolean isEmpty() {
		return (size ==0);
	}
	
	public void add(E newItem) {
		if((rear+1)%q.length==front) {//꽉차있다, rear로 체크하면안된다..
			resize(2*q.length);
		}
		rear=(rear+1)%q.length;
	q[rear]=newItem;
	size++;}
	
	public E remove() {
		if(isEmpty()) {
			throw new NoSuchElementException();
		}
		front=(front+1)%q.length;//계속 빈front를 가리키는 것인가?그럼...(계쏙한칸앞을 가리키고 있기때문에)
		E item = q[front];
		q[front]= null;
		size--;
		if(size>0 && size==q.length/4) {
			resize(q.length/2);}
		return item;
	}
	
	private void resize(int newSize) {

		System.out.println("호출");
		Object [] t = new Object[newSize];
		for(int i=1, j=front+1;i<size+1;i++,j++) {
			t[i]=q[j%q.length];
		}
		front=0;
		rear=size;
		q=(E[]) t;}
	
	public void print() {
		System.out.print("항목수: ");
		System.out.print(size+"/  ");
		for(int i =0; i<q.length;i++) {
			System.out.print(q[i]);
			System.out.print("  ");}
		System.out.println();}
	}
