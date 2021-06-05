package etc;

public class HanoiPractice {

	public static void HanoiStart(int n) {
		int i=1;
		int t=n;
		System.out.println("원반이 "+n+"개인 경우");
		System.out.print("(원반 이름: 크기가 작은-큰 순서 ");
		for(i=1;i<=t;i++) {
			System.out.print(i);
			if(i==t) {
				break;
			}
			System.out.print("-");
		}
		System.out.println(")");
		
		System.out.println();
		
	}
	public static void Hanoi(int n, String start, String mid, String fin) {
		if(n==1) {
			System.out.println("으악");
			System.out.println("원반 1을 "+start+"에서 "+fin+"로 이동");
			return;
		};
		Hanoi(n-1, start, fin, mid);
		System.out.println("원반 "+n+"을 "+start+"에서 "+fin+"로 이동");
		Hanoi(n-1, mid, start, fin);
	}
	
	public static void main(String[] args) {
		HanoiStart(3);
		Hanoi(3, "A", "B", "C");
		System.out.println();
		HanoiStart(4);
		Hanoi(4, "A", "B", "C");
		
		
	}

}
