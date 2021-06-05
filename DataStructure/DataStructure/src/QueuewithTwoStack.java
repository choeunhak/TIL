import java.util.Stack;

public class QueuewithTwoStack {

	//큐의 메소드인 add remove 구현

	Stack s1 = new Stack();
	Stack s2 = new Stack();
	public void add(Object o) {
		s1.push(o);
	}
	
	public Object remove() {
		while(true) {
			if(s1.size()==0) {
				break;
			}
			s2.push(s1.pop());
		}
		Object k = s2.pop();
		while(true) {
			if(s2.size()==0) {
				break;
			}
			s1.push(s2.pop());
		}
		return k;
	}
	
	public static void main(String[] args) {
		QueuewithTwoStack q = new QueuewithTwoStack();
		q.add(1);
		q.add(2);
		q.add(3);
		System.out.println(q.remove());
		q.add(4);
		System.out.println(q.remove());
		
	}

}
