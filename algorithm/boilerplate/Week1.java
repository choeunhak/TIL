
public class Week1 {
//아래 for문에 관한 빅오, 빅오메가, 빅세타 표기법을 알아내고 학습하기 위한 코드입니다.
	public static void main(String[] args) {
		
		int s = 0;
		int k=8;
		int i;
		
		for(i=0; i<k;i++) {
			System.out.println("i"+i);
			for(int j=0;j<i;j++) {
				s+=j;
				System.out.println("j"+j);
			}
		}
		System.out.println("s"+s);
		System.out.println("ans"+k*i);
	}

}
