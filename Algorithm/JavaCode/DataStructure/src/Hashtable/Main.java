package Hashtable;

public class Main {
	
	public static void main(String[] args) {
	LinearProbing lp = new LinearProbing();
	lp.put(25, "grape");
	lp.put(37, "apple");
	lp.put(18, "banana");
	lp.put(55, "cherry");
	lp.put(22, "mango");
	lp.put(35, "lime");
	lp.put(50, "orange");
	lp.put(63, "watermelon");
	
//	System.out.println("탐색 결과:");
//	System.out.println("50의 data = "+lp.get(50));
//	System.out.println("63의 data = "+lp.get(63));
//	System.out.println();
//	System.out.println("해시 테이블: ");
//	lp.print();
//	System.out.println();
//	

	QuadProbing qp = new QuadProbing();
	qp.put(25, "grape");        
	qp.put(37, "apple");        
	qp.put(18, "banana");       
	qp.put(55, "cherry");       
	qp.put(22, "mango");        
	qp.put(35, "lime");         
	qp.put(50, "orange");       
	qp.put(63, "watermelon");   
//	System.out.println("탐색 결과:");
//	System.out.println("50의 data = "+qp.get(50));
//	System.out.println("63의 data = "+qp.get(63));
//	System.out.println();
//	System.out.println("해시 테이블: ");
//	qp.print();
//	System.out.println();
	

	DoubleHashing dh = new DoubleHashing();
	dh.put(25, "grape");        
	dh.put(37, "apple");        
	dh.put(18, "banana");       
	dh.put(55, "cherry");       
	dh.put(22, "mango");        
	dh.put(35, "lime");         
	dh.put(50, "orange");       
	dh.put(63, "watermelon");   
//	System.out.println("탐색 결과:");
//	System.out.println("50의 data = "+dh.get(50));
//	System.out.println("63의 data = "+dh.get(63));
//	System.out.println();
//	System.out.println("해시 테이블: ");
//	dh.print();
//	System.out.println();
	

	Chaining c = new Chaining();
	c.put(25, "grape");        
	c.put(37, "apple");        
	c.put(18, "banana");       
	c.put(55, "cherry");       
	c.put(22, "mango");        
	c.put(35, "lime");         
	c.put(50, "orange");       
	c.put(63, "watermelon");
	
	System.out.println("탐색 결과:");
	System.out.println("50의 data = "+lp.get(50));
	System.out.println("63의 data = "+lp.get(63));
	System.out.println("37의 data = "+lp.get(37));
	System.out.println("22의 data = "+lp.get(22));
	System.out.println();
	System.out.println("해시 테이블: ");
	c.print();
	}                                                                 
	                                                                  
                                                                      
                                                                      
}                                                                     
