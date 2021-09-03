package Sort;

public class Main {

	public static void main(String[] args) {
		Heap s = new Heap();
	    Comparable[] li = new Comparable[13];
	    li[0] = null; 
	    li[1] = 65; 
	    li[2] = 95; 
	    li[3] = 90; 
	    li[4] = 80;
	    li[5] = 55; 
	    li[6] = 70; 
	    li[7] = 35; 
	    li[8] = 50;
	    li[9] = 10; 
	    li[10] = 25; 
	    li[11] = 40; 
	    li[12] = 30;
	    s.sort(li);
	    for (int i = 1; i < 13; i++) 
	    	System.out.print(li[i]+" ");
	}
}


//Shell s = new Shell();
//Comparable[] li = new Comparable[12];
//li[0] = 65; 
//li[1] = 95; 
//li[2] = 90; 
//li[3] = 80;
//li[4] = 55; 
//li[5] = 70; 
//li[6] = 35; 
//li[7] = 50;
//li[8] = 10; 
//li[9] = 25; 
//li[10] = 40; 
//li[11] = 30;
//s.sort(li);
//for (int i = 0; i < 12; i++) 
//	System.out.print(li[i]+" ");