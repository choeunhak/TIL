#오존에 영향을 미치는 요인분석

airquality

#NA 값있는지 확인
col1 = mapply(anyNA, airquality)
col1

#오존과 솔라는 NA값이 있다
#빼버리면 선형회귀모델 만드는 것이 부실해질수있다
#NA를 특정수치로 바꾼다, 대체하는 최대한의 값이 NA의 달이 나머지 해당일의 평균으로 대체해버림


# Compute monthly mean in Ozone
for (i in 1:nrow(airquality)){
  if(is.na(airquality[i,"Ozone"])){
    airquality[i,"Ozone"]<- mean(airquality[which(airquality[,"Month"]==airquality[i,"Month"]),"Ozone"],na.rm = TRUE)
  }
# Compute monthly mean in Solar.R
  if(is.na(airquality[i,"Solar.R"])){
    airquality[i,"Solar.R"]<- mean(airquality[which(airquality[,"Month"]==airquality[i,"Month"]),"Solar.R"],na.rm = TRUE)
  }
}

#NA값이 없는 상태가 됨

airquality

#solar에 비해서 wind가 수치적으로 차이가 적기때문에 영향을 미치는지 애매하다
#근데 실제로 wind도 영향을미치고있다
#regression모델에서 하나의 숫자가 크면 동등한 비교가 안될수있다
#각모든변수가 동일한 범위의 range로 바꾸도록해버리자

#다 0~1로 정규화시켜버림

normalize = function(x){
  return((x-min(x))/(max(x)-min(x)))
}
airquality = normalize(airquality)
str(airquality)
head(airquality)

install.packages("corrplot")
library(corrplot)
airquality_cor = cor(airquality)
corrplot(airquality_cor,method="color", type="lower", addCoef.col="black")

#바람과 오존은 음의 상관관계
#solar, 온도와 오존은 양의 상관관계

#solar와 오존의 상관관계
Y=airquality[,"Ozone"]
X=airquality[,"Solar.R"]
model1 = lm(Y~X)
model1
plot(Y~X)
abline(model1, col="blue", lwd=3)

summary(model1)
#대개의 경우 x에따라 y가 증가하는 모델을 이선형회귀모델이 설명해줄수있다
#전체양의 7퍼센트는 설명이 되어진다
#28분

#model2
#wind와 오존의 상관관계
Z=airquality[,"Wind"]
model2 = lm(Y~Z)
model2
plot(Y~Z)
abline(model2, col="blue", lwd=3)
summary(model2)
#음의상관관계를 가진다


#예측시각화
airquality$forecast=predict(model_total)
library(ggplot2)
ggplot(data=airquality,aes(x=Ozone,y=forecast))+geom_point()+geom_smooth(method=lm)+labs(title="airquality linear regression model")

#ozone 농도를 예측하는 최상의 선형회귀모델을 만들어라
#solar wind, temp 여러가지를 조합해서 좋은 선형회귀모델을 구해라