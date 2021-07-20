package UnionFindTest;

public class Main {

	public static void main(String[] args) {

		int N=11;
		Node[] a =new Node[N];
		
		for(int i=0;i<N;i++) {
			a[i] = new Node(i,0);
		}

		UnionFind uf = new UnionFind(a);
		
		uf.union(3, 10);
		uf.union(3, 0);
		uf.union(3, 8);
		
		
		uf.union(5, 7);

		uf.union(9, 1);
		uf.union(9, 5);
		
		
		uf.union(4, 2);
		uf.union(4, 6);
	
		for(int i=0;i<N;i++) {
			System.out.print("("+i+":"+uf.a[i].getParent()+","+uf.a[i].getRank()+")");
		}
		
		uf.union(10, 7);
		
		System.out.print("\n\nunion(9,1) 수행 후\n(i:parent,rank):");
		for(int i=0;i<N;i++) {
			System.out.print("("+i+":"+uf.a[i].getParent()+","+uf.a[i].getRank()+")");
		}
		System.out.println();
		
	}
}
