
plot(10:1)


close.screen(all=TRUE)

split.screen(c(2,1))
split.screen(c(1,3), screen=2)

screen(1)
plot(10:1)
screen(4)
plot(1:10)



#그래프 지우기
dev.off()



x=seq(1,10,0.1)
y=exp(x)

#산포도 그래프
plot(x,y)

#선모양으로 바구기
plot(x,y, type="l")

plot(x,y, type="l", col="blue", lty=2)
title("Exponential Value")



#toothgrowth 기니피그 치아길이와 비타민의 관계 연구


data(ToothGrowth)
head(ToothGrowth)

dim(ToothGrowth)

plot(ToothGrowth)

plot(ToothGrowth$len, ToothGrowth$dose, main="Tooth Growth according to Dose", xlab="Length", ylab="Dose")


B=c(110,300,150,280,310)
S=c(180,200,210,190,170)
P=c(210,150,260,210,70)

B_type=matrix(c(B,S,P), 5,3)

B_type

#범례 박스 생성, cex는폰트크기를 현재폰트 기준으로 0.5이다,  fill은 색깔!
legend(1,400, c("A","B"), cex=0.5)
#1,400은 x y 좌표임

#t(B_type)하면 tranfer됨

x=c(1:9)
y=x*2
z=x*3

plot(x,y,type="o")

points(x,z,pch="+")#점만 그려줌
lines(x,z,col="blue")#점을 이어줌
#근데 이렇게 그리면 점을이어준선그래프가 짤리게된다


dotchart(x,z,pch=22)#이렇게하면 덮여씌워져서 다 사라짐



#boxplot

A=c(110,300,150,280,310)
B=c(180,200,210,190,170)
C=c(210,150,260,210,70)

boxplot(A,B,C, col=c("yellow", "cyan", "green"),
        names=c("baseball", "soccerball", "pingpong"),
        horizontal=F)


dev.off()

#iris boxplot
data(iris)
plot(iris$Sepal.Width)

sepal.stat1=boxplot(iris$Sepal.Width)
sepal.stat1


sepal.stat2=boxplot(Sepal.Width ~Species, data=iris, col=c("blue", "green", "red"))
sepal.stat2

sepal.stat2=boxplot(Sepal.Width ~Species, data=iris, notch=T,col=c("blue", "green", "red"))
sepal.stat2


dev.off()

#레이아웃 만들기
boxplot_hist=layout(matrix(c(1,2,2), 3,1, byrow=TRUE))#3행 1열로 만들
layout.show(boxplot_hist)#레이아웃을 보여주라라
boxplot(iris$Sepal.Length, horizontal=TRUE, col="green1")
hist(iris$Sepal.Length,xlim=c(4,8), col="pink",freq=FALSE)
lines(density(iris$Sepal.Length))#밀도 보여주기

#밀도가 위랑 아래랑 어느정도 일치한다!!!

#hist_boxplot


table(mpg$manufacturer)#빈도수조사사

