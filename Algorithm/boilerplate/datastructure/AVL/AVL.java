package AVL;

import java.util.LinkedList;
import java.util.Queue;


public class AVL<Key extends Comparable<Key>, Value>{
	  public Node root;
	  
	  public AVL(){
	    root = null;
	  }
	  
	  // 탐색
	  public Value get(Key k){return get(root, k);}
	  public Value get(Node n, Key k){
	    if (n == null) 
	    	return null; // k를 발견 못함
	    
	    int t = n.getKey().compareTo(k);
	    if (t > 0) 
	    	return get(n.getLeft(), k); // if (k < 노드 n의 id) 왼쪽 서브트리 탐색
	    else if (t < 0) 
	    	return get(n.getRight(), k); // if (k > 노드 n의 id) 오른쪽 서브트리 탐색
	    else 
	    	return (Value) n.getValue(); // k를 가진 노드 발견
	  }
	  
	  // 삽입 연산
	  public void put(Key k, Value v){
		  root = put(root, k, v);}
	  
	  public Node put(Node n, Key k, Value v){
	    if (n == null) return new Node(k,v,1);
	    
	    int t = k.compareTo((Key) n.id);
	    if (t < 0) 
	    	n.setLeft(put(n.getLeft(), k, v)); // 왼쪽 서브트리에 삽입
	    else if (t > 0)
	    	n.setRight(put(n.getRight(), k, v)); // 오른쪽 서브트리에 삽입
	    else {
	    	n.name=v;
	    	return n;} // 노드 n의 name을 v로 갱신
	    
	    n.height = tallerHeight(height(n.left), height(n.right))+1;
	    return balance(n);
	  }
	  
	  private Node balance(Node n) {
		 
		if(bf(n)>1) {
			if(bf(n.left)<0) {
				n.left=rotateLeft(n.left);
			}
			n=rotateRight(n);
		}
		else if(bf(n)<-1) {
			if(bf(n.right)>0) {
				n.right=rotateRight(n.right);
			}
			n=rotateLeft(n);
		}
		
		return n;
	}

	private Node rotateRight(Node n) {
		Node x = n.left;
		n.left = x.right;
		x.right = n;
		//높이갱신
		n.height = tallerHeight(height(n.left), height(n.right))+1;
		x.height = tallerHeight(height(x.left), height(x.right))+1;
		return x;
	}

	private Node rotateLeft(Node n) {
		Node x = n.right;
		n.right = x.left;
		x.left = n;
		//높이갱신
		n.height = tallerHeight(height(n.left), height(n.right))+1;
		x.height = tallerHeight(height(x.left), height(x.right))+1;
		return x;
	}
	
	public void delete(Key k) {
		root = delete(root,k);
	}

	private Node delete(Node n, Key k) {
		if(n==null) {
			return null;
		}
		int t = k.compareTo((Key)n.id);
		
		if(t<0) {
			n.left = delete(n.left, k);
		}
		else if(t>0) {
			n.right = delete(n.right, k);
		}
		else {
			if(n.left==null) {
				return n.right;
			}
			else if(n.right==null) {
				return n.left;
			}
			else {
				Node target=n;
				n=min(target.right);
				n.right=deleteMin(target.right);
				n.left=target.left;
			}
		}
		
		n.height = tallerHeight(height(n.left), height(n.right))+1;
		return balance(n);	}

	private int bf(Node n) {
		return height(n.left) - height(n.right);
	}

	private int tallerHeight(int x, int y) {
		if(x>y) {
			return x;
		}
		else {
			return y;
		}
	}

	// 최솟값 찾기
	  public Key min(){
	    if (root == null) return null;
	    
	    return (Key) min(root).id;
	  }
	  private Node min(Node n){
	    if (n.getLeft() == null) 
	    	return n;
	    
	    return min(n.getLeft());
	  }
	  
	  // 최솟값 삭제 연산
	  public void deleteMin(){
	    if (root == null)
	    System.out.println("empty 트리");
	    
	    root = deleteMin(root);
	  }
	  public Node deleteMin(Node n){
	    if (n.getLeft() == null) 
	    	return n.getRight(); // if (n의 왼쪽자식 == null) n의 오른쪽자식 리턴
	    
	    n.setLeft(deleteMin(n.getLeft())); // if (n의 왼쪽자식 != null), n의 왼쪽자식으로 재귀호출
	    n.height = tallerHeight(height(n.left), height(n.right))+1;
	    return balance(n);
	  }
	  
	  public int height(Node n) {
			if(n==null)
				return 0;
				
			return n.height;}
		
	  public void print(Node root) {
		  System.out.printf("\ninorder:\n");
		  inorder(root);
		  System.out.printf("\npreorder:\n");
		  preorder(root);
		  System.out.printf("\nlevel order:\n");
		  levelorder(root);
	  }
		
	  public void preorder(Node n) {
			if(n!=null) {
				System.out.print(n.getKey()+" ");
				preorder(n.getLeft());
				preorder(n.getRight());}}
		
		public void inorder(Node n) {
			if(n!=null) {
				inorder(n.getLeft());
				System.out.print(n.getKey()+" ");
				inorder(n.getRight());}}
		
		public void levelorder(Node root) {
			Queue<Node> q = new LinkedList<Node>();
			Node t;
			
			q.add(root);
			while(!q.isEmpty()) {
				t=q.remove();
				System.out.print(t.getKey()+" ");
				
				if(t.getLeft()!=null) {
					q.add(t.getLeft());}
				if(t.getRight()!=null) {
					q.add(t.getRight());}}}
}
		
		
	  
	  
	