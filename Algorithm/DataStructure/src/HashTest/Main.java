package HashTest;

public class Main {
	
	public static void main(String[] args) {
	LinearProbing lp = new LinearProbing();
	QuadProbing qp = new QuadProbing();
	DoubleHashing dh = new DoubleHashing();
	Chaining c = new Chaining();
	lp.put(71, "grape");
	lp.put(23, "apple");
	lp.put(73, "banana");
	lp.put(49, "cherry");
	lp.put(54, "mango");
	lp.put(89, "lime");
	lp.put(39, "orange");
	
	System.out.println("탐색 결과:");
	System.out.println();
	System.out.println("해시 테이블: ");
	lp.print();
	System.out.println();
	
	qp.put(71, "grape");        
	qp.put(23, "apple");        
	qp.put(73, "banana");       
	qp.put(49, "cherry");       
	qp.put(54, "mango");        
	qp.put(89, "lime");         
	qp.put(39, "orange");       
	   
	System.out.println("탐색 결과:");
	System.out.println();
	System.out.println("해시 테이블: ");
	qp.print();
	System.out.println();
	
	dh.put(71, "grape");        
	dh.put(23, "apple");        
	dh.put(73, "banana");       
	dh.put(49, "cherry");       
	dh.put(54, "mango");        
	dh.put(89, "lime");         
	dh.put(39, "orange");       
	  
	System.out.println("탐색 결과:");
	System.out.println();
	System.out.println("해시 테이블: ");
	dh.print();
	System.out.println();
	
	c.put(71, "grape");        
	c.put(23, "apple");        
	c.put(73, "banana");       
	c.put(49, "cherry");       
	c.put(54, "mango");        
	c.put(89, "lime");         
	c.put(39, "orange");       
	
	System.out.println("탐색 결과:");
	System.out.println();
	System.out.println("해시 테이블: ");
	c.print();
	}                                                                 
	                                                                  
                                                                      
                                                                      
}                                                                     
