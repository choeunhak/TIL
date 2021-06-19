#iris data 피어슨상관계수 구하기

cor(iris$Sepal.Width, iris$Sepal.Length)
#수 값이 작아 두 값 사이에 큰 상관 관계는 없으나, 
#Sepal.Width 가 커짐에 따라 Sepal.Length가 작아지는 경향이 있음

#species를제외한 모든 컬럼의 피어슨 상관계수
cor(iris[,1:4])#보기어려움움

#symnum
#복잡한상관계수를단순하게 표현
symnum(cor(iris[,1:4]))


library(corrgram)
corrgram(iris,upper.panel = panel.conf)

#대각선을 기준으로 대칭이다!!
#신뢰구간의값도보여준다다
#귀무가설->상관계수가 0이다
#대립가설->0이 아니다, 관련이 있다!!

cor.test(c(1,2,3,4,5),c(1,0,3,4,5),method = "pearson")
cor.test(c(1,2,3,4,5),c(1,0,3,4,5),method = "kendall")
#어느정도로 관련이 있을까?->0.914 강한 양적 상관관계

#피어슨 말고 시프어맨 캔들을 이용해서 상관계수가
#더 작은 숫자를 사용하는 것이 바람직

#실제데이터분석

#실업자수가 증가하면 개인소비지출이 감소할까??

data = as.data.frame(economics)
cor.test(data$unemploy, data$pce)
#default는 피어슨
#피벨류가 매우 작고 대립가설 채택!!
#독립이 아니다! 관계가 있다!
#95퍼센트의 신뢰도로 0.56~ 0.66
#0.61정도의 값



#mtcars 상관분석
head(mtcars)
car_cor = cor(mtcars)
round(car_cor, 2)
install.packages("corrplot")
library(corrplot)
corrplot(car_cor)
#히트맵그리기기
corrplot(car_cor,
         method = "color", #method: circle, square.ellipse, number, shade, color, pie
         order="FPC", #order: AOE, hclust, FPC, alphabet
         addCoef.col = "black",
         tl.col = "black", tl.srt = 45, diag = F)
#hclust군집!! fpc-주성분 순서대로 aoe 벡터 순서대로
