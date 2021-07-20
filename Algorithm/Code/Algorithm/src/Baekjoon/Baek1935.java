package Baekjoon;
import java.util.*;


public class Baek1935 {

	public static void main(String[] args) {
		Stack<Double> stack = new Stack<>();
		ArrayList<Object> num = new ArrayList<Object>();
		Queue<Double> que = new LinkedList<Double>();
		Scanner sc = new Scanner(System.in);
		int k=sc.nextInt();
		String sik=sc.next();
		for(int t=0;t<k;t++) {
			int p=sc.nextInt();
			que.add((double) p);
		}
		
		String[] sp = sik.split("");
		
		int A =65;
		
		for(int i=0;i<sp.length;i++) {
			String a=Character.toString(A);
			if(sp[i].equals(a)) {
				num.add(que.remove());
				A++;
			}
			else {
				num.add(sp[i]);
			}
		}
		
		//숫자면 스택에 넣고
		//아니면 
		
		for(int i = 0; i<num.size();i++) {
			double result=0;
			double num1=0;
			double num2=0;

			if(num.get(i).equals("+")) {

				num1=(double) stack.pop();
				num2=(double) stack.pop();
				result=num2+num1;
				stack.push(result);
			}
			else if(num.get(i).equals("-")) {
				num1=(double) stack.pop();
				num2=(double) stack.pop();
				result=num2-num1;
				stack.push(result);
				
			}
			else if(num.get(i).equals("*")) {
				num1=stack.pop();
				num2=(double) stack.pop();
				result=num2*num1;
				stack.push(result);
				
			}
			else if(num.get(i).equals("/")) {
				num1=(double) stack.pop();
				num2=(double) stack.pop();
				result=num2/num1;
				stack.push(result);
				
			}
			else {
				stack.push((Double) num.get(i));
			}
		}
		System.out.println(String.format("%.2f", stack.pop()));

	}

}
