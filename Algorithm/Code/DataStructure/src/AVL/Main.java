package AVL;

public class Main {
	  public static void main(String[] args) {
	    AVL<Integer, String> st = new AVL<Integer, String>();
	    
	    
	    st.put(75, "Apple");
	    st.put(80, "Grape");
	    st.put(85, "Lime");
	    st.put(20, "Mango");
	    st.put(10, "Strawberry");
	    st.put(50, "Banana");
	    st.put(30, "Cherry");
	    st.put(40, "Watermelon");
	    st.put(70, "Melon");
	    st.put(90, "fruit");
	    
	    
	    st.print(st.root);
	    System.out.println();
	    System.out.println("높이 = "+st.height(st.root));
	    System.out.println("\n75,85,50 삭제 후 >>");
	    st.delete(75);
	    st.delete(80);
	    st.delete(50);
	    
	    st.print(st.root);
	    System.out.println();
	    
	  }
	}
