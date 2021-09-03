package Baekjoon;
import java.util.Scanner;
import java.util.Stack;

public class Baek11899 {

	public static void main(String[] args) {
		
		Stack st = new Stack();
		Scanner sc = new Scanner(System.in);
		String s = sc.next();
		int ans=0;
		int i =0;
//		while(true) {
//			if(s.charAt(i)==('(')) {
//				s=s.substring(i,s.length());
//				break;
//			};
//			i=i+1;
//			ans=ans+1;
//		}
		for(int t =0; t<s.length();t++) {
			if(s.charAt(t)=='(') {
				st.push(s.charAt(t));
			}
			else {
				if(st.isEmpty()==true){
					ans++;
				}
				else {
					st.pop();
				}
			}
				
		}

		System.out.println(ans+st.size());
	}

}
