#1
dat=iris

dat$size=ifelse(dat$Sepal.Length<median(dat$Sepal.Length),'small','big')

#독립성 검정
SizeSpecies=xtabs(~size+Species, data=dat)
chisq.test(SizeSpecies)
#p-value가 0.05보다 매우 작은 값으로 size와 species는 독립이 아니다

#참고
dat.aov=aov(dat$Sepal.Length~dat$Species)
summary(dat.aov)
#p value는 0.05보다 매우 작은 값이다.
#species 내 차이보다 species 간의 차이가 크다.
#Sepal의 length size는 species(종)별로 다르다고 할 수 있다.


#평균 비교하는 거는 ttest를 수행한다
#2
group=c(rep("Woman",9), rep("Man",9))
weight=c(38.9, 61.2, 73.3, 21.8, 63.4, 64.6, 48.4, 48.8, 48.5, 67.8, 60.0, 63.4, 76.0, 89.4, 73.3,67.3, 61.3, 62.4)

#정규성 가정
shapiro.test(weight)
# pvalue가 0.27로 정규분포를 만족한다

#분산의 동질성 가정
var.test(weight[1:p], weight[10:18])
# 분산이 0.68~ 8.73 사이의 값으로 분산은 동질하다

# 각각의 모집단에서 표본들이 독립적으로 표집되었다고 가정한다.

res.aov=aov(weight~group)
summary(res.aov)
#F값은 7.752로 평균치로 보았을때 분자부분에는 그룹간 차이로 1283, 분모에는 그룹 내 차이로 165기 때문에
#그룹간 차이보다 그룹 내 차이가 작다, 즉, 그룹안에서의 차이보다 그룹 간의 차이가 더 크다
#그리고 pvalue가 0.01로 0.05보다 작기 때문에 의미가 있다(별은 한개다)
#귀무가설이 아닌 대립가설을 선택한다
#여성과 남성의 몸무게의 평균은 다르다고 할 수 있다











#평균간의 비교는 ttest다
#paired는 관련된 집단인지 아닌지에 따라 달라지는듯(같은 id는 같은 id끼리)
#일반적으론 false

#교수님 답
group=c(rep("Woman",9), rep("Man",9))
weight=c(38.9, 61.2, 73.3, 21.8, 63.4, 64.6, 48.4, 48.8, 48.5, 
         67.8, 60.0, 63.4, 76.0, 89.4, 73.3,67.3, 61.3, 62.4)

dat2=data.frame(group,weight)
with(dat2, t.test(weight[group=="Woman"], weight[group=="Man"],paired=FALSE))
#p값이 0.015로 0.05 보다 작다. 따라서 대립가설을 채택한다. 
#따라서 여성과 남성의 몸무게의 평균은 다르다. 
#귀무가설에 의한 모집단의 평균의 차이는 0이어야 하는데, 
#추정한 신뢰구간은 -29.9와 -3.7사이여서 0이 포함되지 않는 것도 확인된다