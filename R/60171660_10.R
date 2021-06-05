#1
dat=iris

dat$size=ifelse(dat$Sepal.Length<median(dat$Sepal.Length),'small','big')

#독립성 검정
SizeSpecies=xtabs(~size+Species, data=dat)
chisq.test(SizeSpecies)
#p-value가 0.05보다 매우 작은 값으로 size와 species는 독립이 아니다

dat.aov=aov(dat$Sepal.Length~dat$Species)
summary(dat.aov)
#p value는 0.05보다 매우 작은 값이다.
#species 내 차이보다 species 간의 차이가 크다.
#Sepal의 length size는 species(종)별로 다르다고 할 수 있다.


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
