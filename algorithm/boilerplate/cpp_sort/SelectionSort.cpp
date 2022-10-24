//선택정렬 가장 작은 것을 선택해서 제일 앞으로 보낸다

#include <stdio.h>

	//시간복잡도
	//얼마나 많은 시간??
	//1~10까지 10번
	//10+9+8+7...+1
	//-->등차수열 10*(10+1)/2==55
	//N*(N+1)/2-->N*N이라고 수행시간,,, bigO표기법
	 //비효율적임 
	 
	 
int main(void){
	int i, j, min, index, temp;
	int array[10]= {1,10, 5, 8, 7, 6, 4, 3, 2, 9};
	for(i=0; i<10; i++){
		min=9999;
		for(j=i;j<10;j++){
			if(min>array[j]){
				min=array[j];
				index=j;
			}
		}//한번 탐색이 끝났을대 가장 작은값이 선됨택이 
		temp=array[i];//일시적으로 맨앞의 값 넣어줌 
		array[i]=array[index];//최솟값을 다시 넣어줌 
		array[index]=temp;//다시 인덱스에 temp에 있던값을 넣어줌
		//스와핑을한다
		 
	};
	
	//정렬이 된 이후에 출력
	for(i=0; i<10; i++){
		printf("%d", array[i]);
	} 
	return 0;
	
	
}
