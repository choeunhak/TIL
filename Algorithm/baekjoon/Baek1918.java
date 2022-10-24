import java.util.*;


public class Baek1918 {

	public static void main(String[] args) {
		
		Stack<String> stack = new Stack<>();
		Scanner sc = new Scanner(System.in);
		String s=sc.next();
		String[] sp = s.split("");
		String result="";
		for(int i=0;i<s.length();i++) {
			if(sp[i].equals("(") ) {
				stack.push(sp[i]);
			}
			else if(sp[i].equals(")")) {
				while(true) {
					if(stack.isEmpty()==true) {
						break;
					}
					String temp=(String) stack.pop();
					if(temp.equals("(")) {
						break;
					}
					else {
						result=result+temp;
					}
				}
			}

			else if(sp[i].equals("+") || sp[i].equals("-")) {
				while(true) {
					if(stack.isEmpty()==true) {
						break;
					}
					if(stack.peek().equals("(")) {
						break;
					}
					else if(stack.peek().equals("+")|| stack.peek().equals("-") || stack.peek().equals("*")|| stack.peek().equals("/")){
						result=result+stack.pop();
					}
				}
				stack.push(sp[i]);
				
			}
			else if(sp[i].equals("*") || sp[i].equals("/")) {
				while(true) {
					if(stack.isEmpty()==true) {
						break;
					}
					if(stack.peek().equals("+")|| stack.peek().equals("-") || stack.peek().equals("(")) {
						break;
					}
					else {
						result=result+stack.pop();
					}
				}
				stack.push(sp[i]);
				
			}
			else {
				result=result+sp[i];
			}
		}
		while(stack.isEmpty()==false){
			result=result+stack.pop();
		}
		
		System.out.println(result);

	}

}
