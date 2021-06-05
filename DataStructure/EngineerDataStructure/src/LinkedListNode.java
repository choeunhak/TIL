

class LinkedList{
	Node header;
	static class Node{
		int data;
		Node next = null;
	}
	LinkedList(){
		header=new Node();
	}
	
	void append(int d) {
		Node end = new Node();//노드생성
		end.data=d;
		Node n= header;//지금의 노드
		while(n.next!=null) {//끝까지감
			n=n.next;
		}
		n.next=end;
	}
	
	void delete(int d) {
		Node n = header;
		while(n.next!=null) {
			if(n.next.data==d) {
				n.next=n.next.next;
			}
			else {
				n=n.next;
			}
		}
	}
	
	void retrieve() {
		Node n=header.next;
		while(n.next!=null) {
			System.out.print(n.data+"->");
			n=n.next;
		}
		System.out.println(n.data);
	}
}


public class LinkedListNode {

	public static void main(String[] args) {

			LinkedList li = new LinkedList();
			li.append(1);
			li.append(2);
			li.append(3);
			li.append(4);
			li.retrieve();
			li.delete(1);//여기서는 첫번째 노드를 지울수 있다
			li.retrieve();
			
			}

}
