package ArrList;
import java.util.NoSuchElementException;

public class ArrList<E> {
	
	private E a[];
	private int size;
	
	public ArrList() {
		a=(E[]) new Object[1];
		size = 0;
	}

	
	public E peek(int k) {
		if(isEmpty())
			throw new NoSuchElementException();

		return a[k];
	}
	
	public boolean isEmpty() {
		return size ==0;
	}
	
	public void insertLast(E newItem) {
		if(size==a.length)
			resize(2*a.length);

		a[size++] = newItem;
	}
	
	public void insert(E newItem, int k) {
		if(size == a.length) 
			resize(2*a.length);
		
		for(int i = size-1; i>=k;i--) {//k다음에 있던 원소들을 한칸씩 뒤로 옮긴다!
			a[i+1] = a[i];
		}
		a[k] = newItem;//그리고 k에 값을 넣는다.
		size++;
	}
	
	private void resize(int newSize) {
		Object[] t = new Object[newSize];//새로운배열
		for(int i =0 ;i<size;i++) {//새로운배열에 원래 배열에 있던 값 넣기
			t[i]  = a[i];
		}
		a = (E[])t;//새로운 배열을 원래배열에 설정
	}
	
	
	public E delete(int k) {
		
		if(isEmpty()) {
			throw new NoSuchElementException();
		}
		
		E item = a[k];
		
		for(int i = k; i<size; i++) {//한칸씩앞으로이동
			a[i] = a[i+1];
		}
		size--;
		
		if(size>0 &&size==a.length/4) {
			resize(a.length/2);
		}
		return item;
	}
	
	
	public void print() {
		for(int i=0;i<this.a.length;i++) {
			if(this.peek(i)!=null) {
				System.out.print(this.peek(i)+ "  ");
			}
			else {
				System.out.print("null"+ "  ");
			}
		}
		System.out.println();
	}
}
