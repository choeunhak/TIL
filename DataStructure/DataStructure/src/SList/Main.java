package SList;

public class Main {

	public static void main(String[] args) {
		
		System.out.println("[연습문제 2.17]");
		SList<Integer> s1 = new SList<Integer>();
		s1.insertFront(9);
		s1.insertFront(5);
		s1.insertFront(1);
		System.out.print("A 링크드리스트 : ");
		s1.print();
		
		SList<Integer> s2 = new SList<Integer>();
		s2.insertFront(10);
		s2.insertFront(7);
		s2.insertFront(6);
		s2.insertFront(3);
		s2.insertFront(2);
		System.out.print("B 링크드리스트 : ");
		s2.print();

		
		SList<Integer> s3 = new SList<Integer>();
		s3.insertFront(-1);
		System.out.print("A와 B가 병합된 링크드리스트 : ");
		s3.merge(s1.head,s2.head);
		s3.print();
		
		System.out.println(" ");
		System.out.println("[연습문제 2.20]");
		
		SList<Integer> s4 = new SList<Integer>();
		s4.insertFront(6);
		s4.insertFront(7);
		s4.insertFront(4);
		s4.insertFront(2);
		s4.insertFront(8);
		s4.insertFront(9);
		System.out.print("원래 링크드리스트 : ");
		s4.print();
		int k = 7;
		
		SList<Integer> s5 = new SList<Integer>();
		SList<Integer> s6 = new SList<Integer>();
		s4.split(k, s5, s6);
		System.out.print(k+"보다 큰 분리된 링크드리스트 : ");
		s5.print();
		System.out.print(k+"보다 작거나 같은 분리된 링크드리스트 : ");
		s6.print();
		
	}

}
