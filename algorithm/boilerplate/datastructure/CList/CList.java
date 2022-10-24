package CList;
import java.util.NoSuchElementException;

import DList.DNode;


public class CList <E extends Comparable<E>>{
	protected Node last;
	private int size;
	public CList() {
		last = null;//마지막노드
		size = 0;
	}
	public void print() {
		if(size>0) {
			int i =0;
		for (Node p =last.getNext(); i<size; p=p.getNext(), i++){
			System.out.print(p.getItem()+"  ");}}
		else {
			System.out.println("리스트 비어있음");}
		System.out.println();
	}
	public int size() { return size;}
	public boolean isEmpty() { return size==0; }
	public void insert(E newItem) {//리스트의 첫노드로 삽입
		Node newNode = new Node(newItem, null);
		
		if(last ==null) {//리스트가 empty일때
			newNode.setNext(newNode);
			last = newNode;}
		else {
			newNode.setNext(last.getNext());
			last.setNext(newNode);}
		size++;}
	public void delete() {//last의 다음노드를 삭제
		if(isEmpty()) throw new NoSuchElementException();
		
		Node x = last.getNext();
		if(x ==last) {//리스트에 한개의 노드만있을때
			last = null;}
		else {
			last.setNext(x.getNext());}
		size--;}}
	

