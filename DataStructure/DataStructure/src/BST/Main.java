package BST;

public class Main {
	  public static void main(String[] args) {
	    BST t = new BST(500, "Apple");
	    t.put(600, "Banana");
	    t.put(200, "Melon");
	    t.put(100, "Orange");
	    t.put(400, "Tangerine");
	    t.put(250, "Kiwi");
	    t.put(150, "Grape");
	    t.put(800, "Strawberry");
	    t.put(700, "Cherry");
	    t.put(50, "Pear");
	    t.put(350, "Lemon");
	    t.put(10, "Watermelon");
	    
	    t.print(t.root);
	    System.out.println();
	    System.out.println("높이 = "+t.height());
	    System.out.println();
	    
	    t.put(400, "Mango");
	    System.out.println("t.get(400) = "+ t.get(400));
	    System.out.println("t.get(800) = "+ t.get(800));
	    System.out.println("t.get(777) = "+ t.get(777));
	    
	    System.out.println("최소 키값 = "+t.min());
	    t.deleteMin();
	    
	    t.print(t.root);
	    System.out.println();
	  }
	}
