import java.util.Scanner;

public class Baek12904 {

	public static void main(String[] args) {
		
		Scanner sc = new Scanner(System.in);
		String s1=sc.next();
		String ans=sc.next();
		
		String temp = ans;
		int result=0;
		if(s1.length()<ans.length() && s1.length()<=999 && s1.length()>=1 &&ans.length()<=1000 && ans.length()>=2 ) {
			while(true) {
				if(s1.equals(temp)) {
					result=1;
					break;
				}
				if(temp.length()<=s1.length()) {
					break;
				}
				if(temp.charAt(temp.length()-1)=='A') {
					temp=temp.substring(0,temp.length()-1);
				}
				else if(temp.charAt(temp.length()-1)=='B') {
					temp=temp.substring(0,temp.length()-1);
					StringBuffer sb = new StringBuffer(temp);
					temp = sb.reverse().toString();
				}
			}
		}
		
		System.out.println(result);
	}

}
