drug=read.csv("./drug.csv")
drug

drug$fatigue=ordered(drug$fatigue, levels=c("low", "med", "high"))
boxplot(dose~fatigue, data=drug, xlab="fatigue", ylab="dose", col=c("blue", "red", "yellow"))

#boxplot으로 보기에 얼추 피로도를 느끼는 집단에 따라 복용량의 차이가 있다

#독립성, 분산의 동질성, 정규성

drug.aov=aov(dose~fatigue,drug)
summary(drug.aov)
#pvalue가 0.0008로 매우 작은값
#fatigue간 차이가 fatigue 내의 차이보다 크다.



TukeyHSD(drug.aov, conf.level = 0.95)
#low-med는 0을 포함한다, 그래서 차이가 존재한다고 할수없다
#high-low에 차이가 존재
#high-med에 차이가 존재

#독립성, 분산의 동질성, 정규성
#plot을 해보면된다!

plot(drug.aov)
#경향의 차이를 본다
#3번째 그림 0을기준으로 특별한 경향이 없다
#4번째 그림을 보는게 좋다
#cook의 거리!
#바깥쪽의 그래프는 outlier 가 확실하다
#20번데이터가 이상치로 보여진다는 것
#20번을 제외하고 아노바분석을해보자

#20번데이터 제거
aov.model2=update(drug.aov, subset(drug, patientID!=20))
summary(aov.model2)
#이상치를 제외해서 pvalue가 매우 작은값으로 결과가 나온다

#2개면 two way anova

aov.model3=aov(dose~fatigue+gender, data=drug)
summary(aov.model3)
#차이가 있다

#두요인아니라 3개의 요인으로도 할수있다
#aov.model1 fatigue
#aov.model3 fatigue, gender
aov.model1=drug.aov
anova(aov.model1, aov.model3)
#두모형이 서로크게 다르지않음, 더 간단한 모형을 선택하면된다
#모델1이 모델2보다 더 좋은 모델!

#올...

warpbreaks
#올에 따라 차이가 있을수있다
#울에 따라
#두개그룹간의 차이-->단순하게
#ttest를 하면된다!평균을 가지고분석을한다 그룹이 3개면 단순평균비교로안돼서
#분산까지 같이고려해야해서 anova


#텐션의 정도에 따라
#아노바 테스트
#그룹이 세개기때문 텐션의 정도에 따라 차이가 난다

#tukey
