import java.util.Scanner;
import java.util.Stack;

public class Baek10733 {
	
	public static void main(String[] args) {
		Stack<Integer> st = new Stack();
		Scanner sc = new Scanner(System.in);

		int ans=0;
		int n= sc.nextInt();
		for(int i =0;i<n;i++) {
			int t= sc.nextInt();
			if(t==0) {
				st.pop();
			}
			else {
				st.push(t);
			}
		}
		while(true) {
			if(st.size()==0) {
				break;
			}
			ans=ans+st.pop();
		}
		System.out.println(ans);
		
		
	}

}
