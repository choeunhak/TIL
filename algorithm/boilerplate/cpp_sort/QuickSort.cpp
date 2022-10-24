//n * logn 되게 작은 숫자임!!

 //퀵정렬 빠르다!!
 
 //특정한 값을 기준으로 큰 숫자와 작은 숫자를 나눈다!!! 두개의 집합으로 나눔
 //기준값을 피벗이라고 함
 //엇갈린다... 
 //재귀함수 구현해야함
 
  
#include <stdio.h>


int number = 10;
int data[10]= {3, 7, 8, 1, 5, 9, 6, 10, 2, 4};


void show(){
	int i;
	for(i=0; i<number; i++){
		printf("%d ", data[i]);
	}
}

void quickSort(int *data, int start, int end){
	if(start>=end){//원소가 한개인 경우 
		return ;
	}
	int key=start; //키는 첫번째 원소
	int i = start+1, j = end, temp; 
	
	while(i<=j){//엇갈릴때까지 반복
	 while(i<=end && data[i]<=data[key]){//키값보다 큰 값을 만날때까지 반복 
	 	i++;
	 } 
	 while(data[j]>=data[key] && j>start){// 키값보다 작은 값을 만날때까지 반복 ,j는 start보다 커야 
	 	j--;
	 } 
	if(i>j){
		temp=data[j];
		data[j]=data[key];
		data[key]=temp;
	} else{
		temp=data[i];
		data[i]=data[j];
		data[j]=temp;
	}
	}
	quickSort(data, start, j-1);
	quickSort(data, j+1, end);
	
}

int main(void){
	quickSort(data, 0, number-1);
	show();
	return 0;
}
