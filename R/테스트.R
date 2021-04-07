x<-2
x
getwd


x<-matrix(1:9, nrow=3)
x

mat3=matrix(1:8, nrow=2)

mat2<-matrix(10:18, nrow=3)
mat2
mat3=x+mat2
mat3

Name=c("철수", "영희", "순이", "영철")
English=c(90,80,60,70)
Math=c(50,60,100,20)

score=data.frame(Name=Name, English=English, Math=Math)
score$AVG=(English+Math)/2
score


v1=c(1,2,3,4,5)
v1
v1=c(1:5)
v1
v1=1:5
v1
v1=seq(from=1, to=5, by=0.5)#간격지정
v1



v2=rnorm(20)#평균은0
v2


mean(v1)

rev(v1)
order(v1)

x=c(1,4,6,7,8)
x[2]
x[-2]#-는 그것만 제외하고
x[-1]
x
x[2<x & x<10]


y=replace(x, c(2), c(30))
x
y



#벡터는 집합이다

#차집합 setdiff



row1=c(1,2,3)
row2=c(4,5,6)
mat1=rbind(row1, row2)
mat1
mat2=cbind(row1,row2)
mat2
#rowbind와 colomubind


#무조건 행부터 채워진다




mat1<-matrix(1:9, nrow=3)
mat1
mat2<-matrix(10:18, nrow=3)
mat2
mat3=mat1+mat2
mat3


#데이터프레임
name=c("철수", "영희", "순이", "영철")
english=c(90,80,60,70)
math=c(50,60,100,20)

score=data.frame(Name=name, English=english, Math=math)


score$AVG=(English+Math)/2 
score
#$연산자 바꿀때 사용

dim(iris)

#Factor
#문자열 데이터는 맞는데범주형 자료의 저장에 사용한다
#ex)성별, 혈액형...문자 말고 범주가 낫다
#이미 지정된 값의 종류 이외의 값이 들어오는 것을 막을 수 있다
f=c('A', 'B', 'B', 'O')
fc=factor(f)

fc[3]
fc[4]='c'
f
fc
as.integer(fc)
#자바의 enumerate-->1, 12월달
#범주지정!


brand=c('M', 'L', 'B')
Menu=c("빅맥", "불고기버거", "치즈와퍼")
Kcal=c('514', '533', '566')
Na=c('917', '817', '920')
Fat=c('15', '13', '12')


burger=data.frame(brand=brand, Menu=Menu, Kcal=Kcal, Na=Na, Fat=Fat)
burger


write.csv(burger,"burger.csv")
#2-1
burger[1,4]
#2-2
burger$Kcal
#2-3
burger[c(1,3),"Menu"]


getwd()

install.packages("dplyr")
library(dplyr)

exam=read.csv("./csv_exam.csv")
exam

exam %>% group_by(class) %>% summarise(mean_math=mean(math))

install.packages("tidyr")
library(tidyr)


install.packages("ggplot2")
library(ggplot2)
mpg
#0321
mpg %>%group_by(class)%>%summarize(mean=mean(cty))

compact=mpg%>%filter(class=="compact")%>%
  group_by(manufacturer)%>%
  summarise(num=n())%>%#빈도수계산
  arrange(desc(num))
compact



#0322
#큐 구현현
q=c()
q_size=9

enqueue = function(data) {
 q<<-c(q,data)
 q_size <<-q_size+1
}


dequeue = function(){
  first=q[1]
  q<<-q[-1]#이게 신기하네네
  q_size <<-q_size-1
  return(first)
}

size=function(){
  return(q_size)
}

#문제점
#외부에서 이 모든게 다 노출이됨..

#큐 function 을 만듬

queue=function(){
q=c()
q_size=9

enqueue = function(data) {
  q<<-c(q,data)
  q_size <<-q_size+1
}


dequeue = function(){
  first=q[1]
  q<<-q[-1]#이게 신기하네네
  q_size <<-q_size-1
  return(first)
}

size=function(){
  return(q_size)
}
 return(list(enqueue=enqueue, dequeue=dequeue, size=size))
}


q=queue()
q$enqueue(1)
queue
q



i=0
for(i in 1:10){
  print(i)
}


i=0
while(i<=30){
  i=i+1
  if(i%%2!=0) next
  print(i)
}




fibo = function(n){
  if(n==1 || n=2){
    return(1)
  }
  return(fibo(n-1)+fibo(n-2))
}



fibolist=function(size){
  
  if(size<=2){
    
    stop("The size should be greater than 2")
    
  }
  
  num1=1
  
  num2=1
  
  fibonacci=c(num1,num2)
  
  count=2
  
  repeat{
    
    count=count+1
    
    if(count>=size) break
    
  }
  
  print(fibonaccci)
  
}



fibo(3)