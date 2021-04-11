#정규분포

x=seq(0,16,length=100)#0부터 16리터 100개로 나눔
y=dnorm(x,mean=7.5,sd=1.5)
plot(x,y,type="l",
     xlab="Litersper day",
     ylab="density",
     main="water children")

pnorm(4, mean=7.5, sd=1.5)


lower=8
upper=15
i=x>=lower & x<upper
#칠하기 ploygon
polygon(c(lower, x[i],upper), c(0, y[i],0), col="red") 
abline(h=0, col="red")

pb=round(pnorm(8,mean=7.5, sd=1.5, lower.tail=FALSE),2)
pb

#employee 데이터분석
employee=read.csv("employees_ex.csv")
str(employee)
hist(employee$incentive, breaks=50)
summary(employee$incentive)
#정규분포가 아니다, 데이터의 모든것을 얘기해줄수없다...이 6개가 데이터의 형태를 


#협상을 한사람들의 그래프가 오른쪽 꼬리가 길다!
hist(employee$incentive[employee$negotiated==FALSE], breaks=50)
hist(employee$incentive[employee$negotiated==TRUE], breaks=50)
#대표값(기초통계량) 형태자체에관한것들을 설명하기에 제한점이있다, 완전히 다른 두그래프가 합쳐져서 보여진것...



#propogate 사용
install.packages("propagate")
library(propagate)
set.seed(275)#난수생성, 과거의난수데이터 저장시키기(재현시키기위해)
observations=rnorm(10000,5)
distTested=fitDistr(observations)

#employee데이터 fit 해보기
incentiveDis=fitDistr(employee$incentive)


#분할표 실습
ctable=data.frame(x=c("3","7","9","10"),
                  y=c("A1", "B2","A1","B2"),
                      num=c(4,6,2,9))

temp=xtabs(num~x+y, data=ctable)
temp
margin.table(temp,1) # 행합
margin.table(temp,2) #열에대한합
margin.table(temp) # 전체합
#테이블에 붙이기기
addmargins(temp, margin=1)
addmargins(temp,margin=2)
addmargins(temp)

#cars93 데이터 실습

library(MASS)

car_table_3=with(Cars93, table(Type,Cylinders))
car_table_3

#왼쪽탭이없음
car_table_4=xtabs(~Type+Cylinders, data=Cars93)
car_table_4

addmargins(car_table_4)

#모자이크 plot그리기
#카테고리컬 데이터를 가시화
library(vcd)
install.packages("vcd")
mosaic(car_table_4, gp=gpar(fill=c("Red","blue")),
       direction="v")

#UC버클리 데이터셋
#성별에 따라 입학허가가 달라지지않을까?
#상대분할표

data("UCBAdmissions")
