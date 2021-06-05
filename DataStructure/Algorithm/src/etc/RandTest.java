package etc;
import java.util.Random;

public class RandTest {

	public static void main(String[] args) {
		
		Random rand = new Random();
		rand.setSeed(10);
		for(int i =0; i<10;i++) {
            System.out.println(rand.nextInt(1000));
		}

	}

}
