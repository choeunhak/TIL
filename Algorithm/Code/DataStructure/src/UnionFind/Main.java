package UnionFind;

public class Main {

	public static void main(String[] args) {

		int N=10;
		Node[] a =new Node[N];
		
		for(int i=0;i<N;i++) {
			a[i] = new Node(i,0);
		}

		UnionFind uf = new UnionFind(a);
		
		uf.union(2, 1);
		uf.union(2, 6);
		uf.union(7, 3);
		uf.union(4, 5);
		uf.union(9, 5);
		uf.union(7, 2);
		uf.union(7, 8);
		uf.union(0, 4);
		
		System.out.print("8회의 union 연산 수행 후\n(i:parent,rank):");
		for(int i=0;i<N;i++) {
			System.out.print("("+i+":"+uf.a[i].getParent()+","+uf.a[i].getRank()+")");
		}
	
		
		uf.union(9, 1);
		
		System.out.print("\n\nunion(9,1) 수행 후\n(i:parent,rank):");
		for(int i=0;i<N;i++) {
			System.out.print("("+i+":"+uf.a[i].getParent()+","+uf.a[i].getRank()+")");
		}
		System.out.println();
		
	}
}
