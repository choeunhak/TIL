#include <stdio.h>
//퀵정렬은 최악의 경우 엔제곱 

//백준 2750 단순정렬 풀이 
int array[1001];//1더해놓는게 정신건가에 이로움 

int main(void){
	
	int number, i, j, min, index, temp;
	scanf("%d", &number);
	for(i=0; i<number; i++){
		scanf("%d", &array[i]);
	} 
	
	for(i=0; i<number; i++){
		min = 1001;
		for(j=i; j<number; j++){
			if(min>array[i]){
			min=array[j];
			index=j;
			}
		}
		temp=array[i];
		array[i]= array[index];
		array[index] = temp;
	} 
	for (i=0; i<number;i++){
		printf("%d\n", array[i]);
	}
};
