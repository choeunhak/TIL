import java.util.Scanner;

public class Baek9935 {
 //계속 돌리다가 같은게 없으면 부셔
	static Scanner sc =  new Scanner(System.in);
	static String s = sc.next();
	static String bomb = sc.next();
	
	static int i =bomb.length();
	
	
	public static String check(String s, String bomb, int i) {
		boolean state=false;
		while(true) {
			if(state==true) {
				break;
			}
			for(int k = 0;k<s.length(); k++) {
				System.out.println(s);
				if(s.substring(k, k+i).equals(bomb)) {
					s=s.substring(0,k)+s.substring(k+i, s.length());
					check(s,bomb,i);
					continue;
				}
				else {
					state=true;
				};
			}
		}
		
		return s;
	}
	public static void main(String[] args) {
		Baek9935 b = new Baek9935();
		if(b.s.length()==0) {
			System.out.println("FRULA");
		}
		else {
			System.out.println(b.check(s, bomb, i));
		}
	}

}
