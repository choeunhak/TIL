import java.util.Scanner;
import java.util.Stack;

public class Baek10799 {
//파이프 레이저로 자르는문제
	public static void main(String[] args) {
		
		Stack<Integer> stack = new Stack<>();
		Scanner sc = new Scanner(System.in);
		String s=sc.next();
		
		String[] sp = s.split("");
		int result=0;
		for(int i =0;i<s.length();i++) {
			if(sp[i].equals("(")) {
				stack.push(i);
			}
			else if(sp[i].equals(")")) {
				if(stack.peek()==i-1) {//레이저인지확인
					stack.pop();
					result=result+stack.size();
				}
				else {//레이저가아니다
                    stack.pop();
                    result++;
                }
				
			}
		}

		System.out.println(result);

	}

}
