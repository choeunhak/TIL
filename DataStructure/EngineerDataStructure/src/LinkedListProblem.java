

//정렬되지 않은 링크드리스트에서 중복된 값을 제거하기, 단 버퍼를 사용하지 않는다
public class LinkedListProblem {

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
