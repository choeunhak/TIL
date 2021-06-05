package ListStack;

import java.util.Scanner;


public class Main {
	
	

	public static void main(String[] args) {
		
		
		ListStack<String> stack = new ListStack<String>();
		
		
		stack.push("apple");
		stack.push("orange");
		stack.push("cherry");
		stack.print();
		System.out.println(stack.peek());
		stack.push("pear");
		stack.print();
		
		stack.pop();
		stack.print();
		
		System.out.println(stack.peek());
		stack.push("grape");
		stack.print();
		

	}

}
