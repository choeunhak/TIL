package ArrayStack;

import java.util.Scanner;

public class Main {
	public static void main(String[] args) {

		
		ArrayStack<String> stack = new ArrayStack<String>();
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





//
//ArrayStack<String> stack = new ArrayStack<String>();
//
//Scanner sc = new Scanner(System.in);
//String k=sc.next();
//String[] sp = k.split("");
//boolean result = stack.correct(sp, stack);
//System.out.println(result);

//
//ArrayStack<String> sta = new ArrayStack<String>();
//
//Scanner sc2 = new Scanner(System.in);
//String t=sc2.next();
//String[] sp2 = t.split("");
//boolean result2 = sta.palin(sp2, sta);
//System.out.println(result2);
