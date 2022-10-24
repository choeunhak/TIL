ad = read.csv("./ad.csv")

par(mfrow=c(2,2))

#1 
#TV �ܼ� ȸ�� �� ����
TV_m = lm(sales~TV, data = ad)

#����
summary(TV_m)

#�ð�ȭ
plot(TV_m)

#2 
#���� �ܼ� ȸ�� �� ����
radio_m = lm(sales~radio, data = ad)

#����
summary(radio_m)

#�ð�ȭ
plot(radio_m)

#3 
#�Ź� �ܼ� ȸ�� �� ����
newspaper_m = lm(sales~newspaper, data = ad)

#����
summary(newspaper_m)

#�ð�ȭ
plot(newspaper_m)


#4
#TV�� ������ ���� ȸ�� �� ����
TV_radio_m = lm(sales~TV+radio, data = ad)

#����
summary(TV_radio_m)

#�ð�ȭ
plot(TV_radio_m)


#5
#TV�� �Ź����� ���� ȸ�� �� ����
TV_news_m = lm(sales~TV+newspaper, data = ad)

#����
summary(TV_news_m)

#�ð�ȭ
plot(TV_news_m)


#6 
#�Ź��� ������ ���� ȸ�� �� ����
news_radio_m = lm(sales~newspaper+radio, data = ad)

#����
summary(news_radio_m)

#�ð�ȭ
plot(news_radio_m)

#7
#TV�� �Ź��� ������ ���� ȸ�� �� ����
tv_news_radio_m = lm(sales~TV+newspaper+radio, data = ad)

#����
summary(tv_news_radio_m)

#�ð�ȭ
plot(tv_news_radio_m)


#8
#TV�� ������ ���� ��ȣ�ۿ� ȸ�� �� ����
TV_radio_m_int = lm(sales~TV*radio, data = ad)

#����
summary(TV_radio_m_int)

#�ð�ȭ
plot(TV_radio_m_int)


#9
#TV�� �Ź����� ���� ��ȣ�ۿ� ȸ�� �� ����
TV_news_m_int = lm(sales~TV*newspaper, data = ad)

#����
summary(TV_news_m_int)

#�ð�ȭ
plot(TV_news_m_int)



#10 
#�Ź��� ������ ���� ��ȣ�ۿ� ȸ�� �� ����
news_radio_m_int = lm(sales~newspaper*radio, data = ad)

#����
summary(news_radio_m_int)

#�ð�ȭ
plot(news_radio_m_int)


#TV�� ������ ���� ��ȣ�ۿ� ȸ�� ���� ���� ���� rsquared ���� ���� ũ�Ƿ� ������ ���� ����



#����

set.seed(100)
#���� �ε���
trainingRowIndex = sample(1:nrow(ad), 0.6*nrow(ad))
ad_trainingData = ad[trainingRowIndex,]
ad_testData = ad[-trainingRowIndex,]


#training data�� �� ����
ad_model = lm(sales~TV*radio, data = ad_trainingData)

#���� ����
ad_pred = predict(ad_model, ad_testData)

#���� ��Ȯ�� ����
actu_pred = data.frame(cbind(actuals=ad_testData$sales, predict=ad_pred))


cor_accuracy=cor(actu_pred)
cor_accuracy