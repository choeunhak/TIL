package ArrayStack;
import java.util.EmptyStackException;//스택에맞게 메세지를 주기 위해 이것을 사용함(전에는 nosuchexception)

public class ArrayStack<E> {
	private E s[];
	private int top;//top항목의 배열원소인덱스
	
	public ArrayStack() {
		s=(E[]) new Object[1];
		top = -1;//빈상태만들기위해 -1로 초기화
		}
	
	
	public E peek() {
		if(isEmpty())
			throw new EmptyStackException();

		//underflow 아무것도 없는상태에서 peek하면 에러가뜸
		return s[top];}
	
	
	public int size() {
		return top+1;}
	
	public boolean isEmpty() {//size가 아니라 top으로 체크함
		return (top==-1);}
	
	public void push(E newItem) {
		if(size()==s.length)
			resize(2*s.length);
		s[++top] = newItem;//top을 증가시키고 새로운 값을 넣음,,size++은 나중에 size를 증가시킴
		}
	
	public E pop() {
		if(isEmpty()) {
			throw new EmptyStackException();}
		E item = s[top];//맨위 아이템 리턴
		s[top--]=null;//top값을 null로한다음에 top값을 하나 줄임
		
		if(size()>0 &&size()==s.length/4) {
			resize(s.length/2);
		}
		return item;
	}
	
	private void resize(int newSize) {
		Object[] t = new Object[newSize];
		for(int i =0 ;i<size();i++) {
			t[i]  = s[i];
		}
		s = (E[])t;
	}
	public void print() {
		if(isEmpty()) {
			System.out.println("스택이 비어있음");
		}
		else for(int i=0;i<size();i++) {
			System.out.print(s[i]+"  ");
		}
		System.out.println();
	}
	
	public void changePostfix() {
		
	}
}
	
	
	
	
	
//public boolean correct(String[] sp, ArrayStack stack) {
//		
//		int i =0;
//		while(i<sp.length) {
//			if(sp[i].equals("(") || sp[i].equals("{") | sp[i].equals("[")) {
//				stack.push(sp[i]);
//			}
//			else if(sp[i].equals("]")){
//				if(!stack.pop().equals("[")) {
//					return false;
//				};}
//			else if(sp[i].equals("}")){
//				if(!stack.pop().equals("{")) {
//					return false;
//				};}
//			else if(sp[i].equals(")")){
//				if(!stack.pop().equals("(")) {
//					return false;
//				};}
//			else {
//				continue;}
//			i++;}
//		return true;}
//	
//	
//		public boolean palin(String[] sp, ArrayStack sta) {
//		
//			if(sp.length%2==1) {//홀수
//				int i =0;
//				while(i<(sp.length/2)) {
//					sta.push(sp[i]);
//					i++;
//				}
//				i=i+1;
//				while(i<sp.length) {
//					sta.print();
//					if(!sta.pop().equals(sp[i])) {
//						return false;
//					}
//					i++;
//				}
//			}
//			else {//짝수
//				int i =0;
//				while(i<sp.length/2) {
//					sta.push(sp[i]);
//					i++;
//				}
//				while(i<sp.length) {
//					if(!sta.pop().equals(sp[i])) {
//						return false;
//					}
//					i++;
//				}
//			}
//		return true;}
