ad = read.csv("./ad.csv")

par(mfrow=c(2,2))

#1 
#TV 단순 회귀 모델 생성
TV_m = lm(sales~TV, data = ad)

#검증
summary(TV_m)

#시각화
plot(TV_m)

#2 
#라디오 단순 회귀 모델 생성
radio_m = lm(sales~radio, data = ad)

#검증
summary(radio_m)

#시각화
plot(radio_m)

#3 
#신문 단순 회귀 모델 생성
newspaper_m = lm(sales~newspaper, data = ad)

#검증
summary(newspaper_m)

#시각화
plot(newspaper_m)


#4
#TV와 라디오로 다중 회귀 모델 생성
TV_radio_m = lm(sales~TV+radio, data = ad)

#검증
summary(TV_radio_m)

#시각화
plot(TV_radio_m)


#5
#TV와 신문으로 다중 회귀 모델 생성
TV_news_m = lm(sales~TV+newspaper, data = ad)

#검증
summary(TV_news_m)

#시각화
plot(TV_news_m)


#6 
#신문과 라디오로 다중 회귀 모델 생성
news_radio_m = lm(sales~newspaper+radio, data = ad)

#검증
summary(news_radio_m)

#시각화
plot(news_radio_m)

#7
#TV와 신문과 라디오로 다중 회귀 모델 생성
tv_news_radio_m = lm(sales~TV+newspaper+radio, data = ad)

#검증
summary(tv_news_radio_m)

#시각화
plot(tv_news_radio_m)


#8
#TV와 라디오로 다중 상호작용 회귀 모델 생성
TV_radio_m_int = lm(sales~TV*radio, data = ad)

#검증
summary(TV_radio_m_int)

#시각화
plot(TV_radio_m_int)


#9
#TV와 신문으로 다중 상호작용 회귀 모델 생성
TV_news_m_int = lm(sales~TV*newspaper, data = ad)

#검증
summary(TV_news_m_int)

#시각화
plot(TV_news_m_int)



#10 
#신문과 라디오로 다중 상호작용 회귀 모델 생성
news_radio_m_int = lm(sales~newspaper*radio, data = ad)

#검증
summary(news_radio_m_int)

#시각화
plot(news_radio_m_int)


#TV와 라디오로 다중 상호작용 회귀 모델을 만든 것이 rsquared 값이 가장 크므로 성능이 가장 좋다



#예측

set.seed(100)
#랜덤 인덱스
trainingRowIndex = sample(1:nrow(ad), 0.6*nrow(ad))
ad_trainingData = ad[trainingRowIndex,]
ad_testData = ad[-trainingRowIndex,]


#training data로 모델 생성
ad_model = lm(sales~TV*radio, data = ad_trainingData)

#예측 수행
ad_pred = predict(ad_model, ad_testData)

#예측 정확성 검증
actu_pred = data.frame(cbind(actuals=ad_testData$sales, predict=ad_pred))


cor_accuracy=cor(actu_pred)
cor_accuracy
