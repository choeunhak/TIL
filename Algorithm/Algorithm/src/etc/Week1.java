package etc;

public class Week1 {
//�Ʒ� for���� ���� ���, ����ް�, ��Ÿ ǥ����� �˾Ƴ��� �н��ϱ� ���� �ڵ��Դϴ�.
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
