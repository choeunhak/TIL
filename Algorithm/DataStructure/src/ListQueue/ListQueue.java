package ListQueue;
import java.util.NoSuchElementException;

public class ListQueue<E> {
	
	private Node<E> front, rear;
	private int size;
	
	public ListQueue() {
		front = rear = null;
		size=0;}
	
	public int size() {
		return size;}
	
	public boolean isEmpty() {
		return (size ==0);}
	
	public void add(E newItem) {
		Node newNode = new Node(newItem,null);
		
		if(isEmpty()) front = newNode;
		else rear.setNext(newNode);;
		rear = newNode;
		size++;}
	
	public E remove() {
		if(isEmpty()) {
			throw new NoSuchElementException();
		}
		E frontItem = front.getItem();
		front = front.getNext();
		size--;
		if(isEmpty()) {//이건뭐지... 하나밖에 없었던 상태(f,r이 같은걸 가리키는 상태), rear도 null이 되게 해줌
			rear=null;}
		return frontItem;}
	
	public void print() {
		Node p =front;
		for(int i =0; i<size;i++) {
			System.out.print(p.getItem());
			System.out.print("  ");
			p=p.getNext();}
		System.out.println();}}
