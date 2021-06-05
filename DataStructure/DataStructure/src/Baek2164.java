
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

public class Baek2164 {

	public static void main(String[] args) {
		
		Scanner sc = new Scanner(System.in);
		int n = sc.nextInt();
		Queue<Integer> arr = new LinkedList<Integer>();
		
		for(int i = 1;i<=n;i++) {
			arr.add(i);
		}
		
		while(true) {
			if(arr.size()==1) {
				break;
			}
			arr.remove();
			arr.add(arr.remove());
		}
		System.out.println(arr.remove());
	}

}
