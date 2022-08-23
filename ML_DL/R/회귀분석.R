#주행속도와 제동거리 사이에 관련이 있는가?
data(cars)

cars
plot(cars$speed, cars$dist)
#상관분석해보기
cor.test(cars$speed, cars$dist, method = "pearson")


m = lm(cars$dist ~ cars$speed, data=cars)
m
#dist=-17.579+3.932*speed + ε 와같은식도출
summary(m)
#Intercept, speed 계수가 통계적으로 유의한지 알려줌
#adjusted rsquared 는 보정된 수치치

#F통계
#회귀모델ㄹ이 종속변수의 분산의 정도를 많은 부분 설명해줄수있따면 
#의미있게 나오고 아니면의미있게 나오지않는다

#축소모델과완전모델간의차이

#축소모델 = 독립변수가고려하지않음 y절편만있고 기울기가없다
#완전모델 = 위에 독립변수 추가
full = lm(cars$dist ~ cars$speed, data=cars)
reduced = lm(cars$dist~1, data=cars)


anova(reduced,full)
#귀무가설 축소모델이 유지된다
#별반차이가없다
#대립가설은 의미가있다

#두개를anova

plot(m)
#아래 예시 참조조
#첫 번째 그래프(왼쪽 위)는 0에 가까울수록 좋은 그래프인데 0에 고르게 분포되어있는 것으로 
#보인다. normal q-q 그래프는 직선에 잘 위치하는 것으로 보아 잔차가 정규분포를 잘 따른
#다. 또한 scale-location 그래프에서는 기울기가 0인 직선이 이상적이고 대부분은 잔차가 0에 
#가깝게 분포되어있지만 몇몇 값들이 잔차가 0에서 멀리 떨어져 있는 것으로 보인다. 네 번째 
#그래프에서는 레버리지가 큰 값들이 존재하지 않는 것으로 보인다.

plot(cars$speed, cars$dist)
abline(coef(m))

#예측
data(cars)
(m=lm(cars$dist~cars$speed, data=cars))
predict(m, newdata = data.frame(speed=3), interval = "confidence")
coef

#예측 및 검정
set.seed(100)
trainingRowIndex = sample(1:nrow(cars), 0.8*nrow(cars))
trainingData = cars[trainingRowIndex,]
testData = cars[-trainingRowIndex,]

lmMod = lm(dist~speed, data=trainingData)
summary(lmMod)

distPred = predict(lmMod, testData)#(testData는 새로운데이터터)
distPred

actuals_preds = data.frame(cbind(actuals = testData$dist, predict=distPred))
head(actuals_preds)

cor_acc = cor(actuals_preds)
cor_acc

#몸무게와 키 분석석
reg = read.csv("regression.csv")
head(reg)
tail(reg)
plot(reg)
plot(reg$weight, reg$height)

cor(reg$height, reg$weight)
#0.967 상관관계가 있다!!

r = lm(reg$height~reg$weight)
r

#키=70.9481 + 1.5218 X 몸무게

abline(r)
summary(r)

plot(r)

#다중회귀
attach(iris)
iris_m=lm(Sepal.Length~Sepal.Width+Petal.Length+Petal.Width, data=iris)
iris_m=lm(Sepal.Length~.,data = iris)
summary(iris_m)
plot(iris_m)
model.matrix(iris_m)[c(1,51,101),]
anova(iris_m)

#세토사가 없는건 3개의 변수를 2개의 가변수로 표현!!!!!!!1

#시각화
with(iris, plot(Sepal.Width, Sepal.Length, cex=.7, pch=as.numeric(Species)))
(m=lm(Sepal.Length~Sepal.Width+Species, data=iris))
coef(m)

abline(2.25,0.80,lty=1)
abline(2.25+1.45,0.80,lty=2)
abline(2.25+1.94,0.80,lty=3)


#상호작용
with(iris, plot(Species, Petal.Length, xlab="Species", ylab="Petal.Length"))
m=lm(Petal.Length~Petal.Width*Species, data=iris)
anova(m)
summary(m)
install.packages("interactions")
library(interactions)
interact_plot(m,pred="Petal.Width",modx="Species", plot.points = TRUE)



#회귀계수 찾기

#Y=X2+3X+5+ε의 회귀 계수를 찾으시오
x=1:1000
y = x^2+3*x+5+rnorm(1000)
lm(y~I(x^2)+x)

#Y=e(X+ ε)의 회귀 계수를 구하시오
x=101:200
y=exp(3*x+rnorm(100))
lm(log(y)~x)

#Y=log(X) + ε 의 회귀 계수를 구하시오
x=101:200
y=log(x)+rnorm(100)
lm(y~log(x))

#절편과 TV계수 모두 pvalue가 0.05보다 매우 작은 값으로 유의미하다고 
#볼 수 있다. adjusted r-squared 값은 1에 가까울수록 좋은 값이기 
#때문에 약 0.61은 그렇게 좋은 수치가 아닌 것을 알 수 있다


#선형회귀정확도 향상

#로그를씌워서 향상시킬수있다

#몸무게와 뇌 무게 선형회귀
library(MASS)
data("mammals")
head(mammals)
attach(mammals)
plot(body, brain)

model1 = lm(brain~body)

summary(model1)
#잔차들이 오른쪽을치우쳐져있는것을알수있다다
plot(model1)

with(mammals, plot(body, brain, log = "xy"))
# data에는 cluster가 있고 몇몇 큰값들이 있음.
#이 차이를 줄이기 위해 log를 취함

model2 = lm(log(brain)~log(body))#log를 씌워서 향상시킬수있다
summary(model2)

par(mfrow=c(2,2), mar=c(2,3,1.5,0.5))
plot(model2)

plot(density(model1$resid), main="model1")
plot(density(model2$resid), main="model2")

#stepwise
#AIC 활용

library(mlbench)
data("attitude")
m=lm(rating~., data=attitude)
m2=step(m, direction = "backward")#방향을지정할수있다다
summary(m2)

data("BostonHousing")
m=lm(medv~., data=BostonHousing)
m2=step(m,direction="both")#빼주는것과 더해주는것을동시에할수있다다
m2

#적은변수로 만드는게 더나을수도있다
#overfitting때문에

#AIC는 2k-2ln(L')
#aic 전체적인값이 작으면작을수록 좋다


library(car)
library(leaps)
library(mlbench)
data("BostonHousing")
#leap subset을 이용하면 모든 경우에 대해 비교할수있음
m=regsubsets(medv~.,data=BostonHousing)
m
summary(m)

plot(m, scale = "adjr2")
plot(m, scale = "bic")
(bestbic = summary(m)$bic)
(min.bic = which.min(bestbic))
coef(m,min.bic)


#이상치 제거
#오렌지나무별 수령과 둘레 저장데이터
data("Orange")
Orange
Orange = rbind(Orange,
               data.frame(Tree=as.factor(c(6,6,6)),
                          age=c(118,484,664),
                          circumference=c(177,50,30)))

with(Orange,
     plot(Tree, circumference, xlab="tree",
          ylab="circumference"))
with(Orange, interaction.plot(age, Tree, circumference))
m=lm(circumference ~ age+I(age^2), data=Orange)
summary(m)
plot(m)

#car패키지에있음, 이상치 테스트를 할수있다
outlierTest(m)
