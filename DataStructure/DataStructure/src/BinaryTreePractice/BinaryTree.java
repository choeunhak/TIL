package BinaryTreePractice;

import java.util.LinkedList;
import java.util.Queue;

public class BinaryTree<key extends Comparable<key>> {
	
	private Node root;
	
	public BinaryTree() {
		root=null;
	}
	public Node getRoot() {
		return root;
	}
	public void setRoot(Node newRoot) {
		root = newRoot;
	}

	public boolean isEmpty() {
		return root==null;
	}
	
	public void preorder(Node n) {
		if(n!=null) {
			System.out.print(n.getKey()+" ");
			preorder(n.getLeft());
			preorder(n.getRight());
		}
	}
	
	public void inorder(Node n) {
		if(n!=null) {
			inorder(n.getLeft());
			System.out.print(n.getKey()+" ");
			inorder(n.getRight());
		}
	}
	
	public void postorder(Node n) {
		if(n!=null) {
			postorder(n.getLeft());
			postorder(n.getRight());
			System.out.print(n.getKey()+" ");
		}
	}
	
	public void levelorder(Node root) {
		Queue<Node> q = new LinkedList<Node>();
		Node t;
		
		q.add(root);
		while(!q.isEmpty()) {
			t=q.remove();
			System.out.print(t.getKey()+" ");
			
			if(t.getLeft()!=null) {
				q.add(t.getLeft());
			if(t.getRight()!=null) {
				q.add(t.getRight());
			}
			}
		}
	}
	
	public int size(Node n) {
		if(n==null) {
			return 0;}
		else {
			System.out.println(n.getKey());
			
			int left = size(n.getLeft());//처음에 여기서끝가지감!
			//System.out.println("left"+left);
			
			int right = size(n.getRight());
			//System.out.println("right"+right);
			
			int ans = 1+left+right;
			System.out.println("ans" + ans);

			//System.out.println();
			return(ans);
			}
	}
	
	public int height(Node n) {
		if(n==null) {
			return 0;
		}
		else {
			return (1+Math.max(height(n.getLeft()), height(n.getRight())));
		}
	}
	
	public static boolean isEqual(Node n, Node m) {
		if(n==null || m==null) {
			return n==m;
		}
		
		if(n.getKey().compareTo(m.getKey())!=0) {
			return false;
		}
		
		return (isEqual(n.getLeft(), m.getLeft()) && isEqual(n.getRight(), m.getRight()));
	}

}
