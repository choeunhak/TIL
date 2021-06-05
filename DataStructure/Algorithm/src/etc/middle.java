package etc;

public class middle {

	public static void abc(int x) {
		System.out.print(x);
		if(x>0) {
			x=x/2;
			abc(x);
		}
		System.out.print(x);
	}
	
	public static void main(String[] args) {
		abc(8);
		

	}

}
