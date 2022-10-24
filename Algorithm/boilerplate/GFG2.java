import java.util.Stack;
  
public class GFG2 {
    static class Queue {
    	static Stack<Integer> s1 = new Stack<Integer>(); 
        static Stack<Integer> s2 = new Stack<Integer>();
		public void enQueue(int x) {
			s1.push(x);
		}
		public int deQueue() {
			int x;
			  
	        //두개의 스택이 비어있으면 에러
	        if (s1.isEmpty() && s2.isEmpty()) {
	            System.out.println("큐가 비어 있습니다.");
	            System.exit(0);
	        }
	        //stack2가 비어있을 때만 stack1에서 stack2로 이동
	        if (s2.isEmpty()) {
	            while (true) {
	            	if(s1.isEmpty()==true) {
	            		break;
	            	}
	            	x = s1.pop();
	                s2.push(x);
	            }
	        }
	        x = s2.pop();
	        return x;
		} 
    }
    public static void main(String args[])
    {
        Queue q = new Queue();
        q.enQueue(1); 
        q.enQueue(2); 
        q.enQueue(3); 
        System.out.println(q.deQueue()); 
        q.enQueue(4); 
        q.enQueue(5); 
        System.out.println(q.deQueue()); 
        System.out.println(q.deQueue());
        System.out.println(q.deQueue()); 
        System.out.println(q.deQueue());
        System.out.println(q.deQueue());
    }
}
