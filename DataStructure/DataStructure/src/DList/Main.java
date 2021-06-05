package DList;

public class Main {

	public static void main(String[] args) {
		
		
		DList<String> s = new DList<String>();
		
		s.insertAfter(s.head, "apple");
		s.print();
		s.insertBefore(s.tail, "orange");
		s.print();
		s.insertBefore(s.tail, "cherry");
		s.print();
		s.insertAfter(s.head.getNext(), "pear");
		s.print();
		
		System.out.println();
		s.delete(s.tail.getPrevious());
		s.print();
		System.out.println();
		s.insertBefore(s.tail, "grape");
		s.print();
		s.delete(s.head.getNext());
		s.print();
		s.delete(s.head.getNext());
		s.print();
		s.delete(s.head.getNext());
		s.print();
		s.delete(s.head.getNext());
		s.print();
		
	}

}
