//삽입정렬  각 숫자를 '적절한 위치'에 삽입한다!!!, 삽입정렬은 필요할때만 위치를 바꾼다 
//선택, 버블은 항상 위치를 바꿈,,
//실제론 더빠름
//이미 앞에건 정렬이 되었음 
//On^2중에선 가장 빠름 
#include <stdio.h>
int main(void){
	int i, j, temp;
	int array[10]= {1, 10, 5, 8, 7, 6, 4, 3, 2, 9};
	for(i=0; i<9; i++){
		j=i;//i를 j에 넣어줌 
		while(array[j]>array[j+1]) {//j는 1씩빼나가면서  오른쪽과 비교를해서 왼쪽이 더 크면 위치를 바꾸어 줌 
		//스와핑 
			temp=array[j];
			array[j]=array[j+1];
			array[j+1]=temp; 
			j--;//궁금증 왜 j++는 안될까?????? 
		}

	};
	
	//정렬이 된 이후에 출력
	for(i=0; i<10; i++){
		printf("%d ", array[i]);
	} 
	return 0;



	
	
}
