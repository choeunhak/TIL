package DList;

public class DNode <E extends Comparable<E>> {
	
	private E item;
	private DNode<E> previous;
	private DNode<E> next;
	
	public DNode(E newItem, DNode<E> p, DNode<E> q) {
		item = newItem;
		previous=p;
		next = q;
	}

	public E getItem() {
		return item;
	}
	public DNode<E> getPrevious() {
		return previous;
	}
	public DNode<E> getNext() {
		return next;
	}
	public void setItem(E newItem) {
		item=newItem;
	}
	public void setPrevious(DNode p) {
		previous = p;
	}
	public void setNext(DNode q) {
		next = q;
	}

}
