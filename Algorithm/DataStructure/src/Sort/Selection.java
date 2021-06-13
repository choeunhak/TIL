package Sort;

public class Selection{
	  public void sort(Comparable[] a){
		    int N = a.length;
		    for (int i = 0; i < N; i++){
		      int min = i;
		      // min 찾기
		      for (int j = i+1; j < N; j++){
		        if (isless(a[j], a[min])) min = j;
		      }
		      swap(a, i, min); // min과 a[i]의 교환
		    }
		  }
	  

	  // 키 비교
	  private boolean isless(Comparable i, Comparable j){
		  return (i.compareTo(j) < 0);
	  }
	  
	  // 원소 교환
	  private void swap(Comparable[] a, int i, int j){
		    Comparable temp = a[i];
		    a[i] = a[j];
		    a[j] = temp;
		  }
		}