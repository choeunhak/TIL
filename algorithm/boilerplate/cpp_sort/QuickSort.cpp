//n * logn �ǰ� ���� ������!!

 //������ ������!!
 
 //Ư���� ���� �������� ū ���ڿ� ���� ���ڸ� ������!!! �ΰ��� �������� ����
 //���ذ��� �ǹ��̶�� ��
 //��������... 
 //����Լ� �����ؾ���
 
  
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
	if(start>=end){//���Ұ� �Ѱ��� ��� 
		return ;
	}
	int key=start; //Ű�� ù��° ����
	int i = start+1, j = end, temp; 
	
	while(i<=j){//������������ �ݺ�
	 while(i<=end && data[i]<=data[key]){//Ű������ ū ���� ���������� �ݺ� 
	 	i++;
	 } 
	 while(data[j]>=data[key] && j>start){// Ű������ ���� ���� ���������� �ݺ� ,j�� start���� Ŀ�� 
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
