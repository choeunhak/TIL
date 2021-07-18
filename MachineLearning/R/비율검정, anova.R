
#비율검정(마치 국민사전투표)
waiting_period = c(3,5,4,5.5,3.5,2.5,3,5,4.5,3,3.5)
above4.hrs=ifelse(waiting_period > 4, "yes","no")
above4hr.table = table(above4.hrs)
above4hr.table

binom.test(4, n=11, p=0.5)
#4/11이 50퍼센트라고얘기할수있는가?
#0.54로 50퍼센트라고얘기할수있다


#binom과 다른건 prop은 비율로 검정

#동전던지기 50%확인
prop.test(42,100)
#신뢰구간 0.32와 0.52사이에 0.5가포함되어있다
#pvalue는 0.13

prop.test(c(57,24),c(407,156))



prop.test(c(110,33),c(201229,200745))


#이표본 비율검정
prop.test(c(45,55),c(100,90))
#pvalue가 0.03으로 동전을던져서 앞면이나올확률은다르다

#남녀승진비율검정
prop.test(c(16,63),c(430,1053))

#ANOVA
xx = c(1,2,3,4,5,6,7,8,9)
yy = c(1.09,2.12,2.92,4.06,4.90,6.08,7.01,7.92,8.94)
zz = c(1.10,1.96,2.98,4.09,4.92,6.10,6.88,7.97,9.01)

mydata = c(xx,yy,zz)#벡터형으로자료생성

mydata
group = c(rep(1,9), rep(2,9), rep(3,9))
group#그룹만들기기
oneway.test(mydata~group, var=T)
# ANOVA 분석의 결과 p-value가 1이므로
#0.05 보다 크기 때문에 3집단이 차이가 없다고
#판단한다







#ANOVA- oneway
my_data = PlantGrowth
my_data
my_data$group = ordered(my_data$group, levels=c("ctrl","trt1","trt2"))

#compute summary
library(dplyr)
group_by(my_data,group) %>% 
  summarise(count = n(),
            mean = mean(weight, na.rm=T),
            sd = sd(weight, na.rm = T))

#visualize the three groups
#boxplot
boxplot(weight~group, data=my_data,
        xlab="Treatment", ylab="weight",
        frame=F, col=c("blue", "yellow", "red"))

#compute the analysis of variance

my_data
res.aov = aov(weight~group, data=my_data)
summary(res.aov)
#분모는 그룹내 차이
#분자는 그룹간차이

#그룹간차이가 group
#그룹내 차이가 residuals
#그룹안에서의 차이보다 그룹간의차이가 더 크다
#P value가 0.05 보다 작으므로, 그룹간의 차이가 유의 하다고 결론 내릴
#수있다
#하지만 어떤것끼리 차이가있는지확인하려면 tukeyHSD를 수행해야한다
TukeyHSD(res.aov)
#trt2와 trt1의 차이만 p value가 0.01이므로 0.05보다 작아서 significant!







#자동차바퀴수명분석
#제조사별로 차이가있을까?

library(ggplot2)
library(dplyr)
tyre = read.csv("tyre.csv")
str(tyre)
summary(tyre)

#브랜드별로 나눠서 boxplot그리기
ggplot(data=tyre, aes(x=Mileage, y=Brands))+geom_boxplot()

tyre %>% group_by(Brands) %>% 
  summarise(N=n(), Mean=mean(Mileage),
            Median = median(Mileage), Min=min(Mileage),
            Max=max(Mileage), SD=sd(Mileage))

#종속변인~독립변인
boxplot(tyre$Mileage~tyre$Brands,
        main="Boxplot comaring Mileage of Four Brands",
        col=rainbow(4),
        horizontal = T)


#브랜드별로 타이어의 수명이 다른디 아노바를 사용하여 분석
tyres.aov=aov(Mileage~Brands,tyre)
summary(tyres.aov)
#Fvalue가 17.9, Pvalue가 매우작은값으로 타이어브랜드별로 수명이 다르다

#어떤 브랜드끼리 다를까?
TukeyHSD(tyres.aov, conf.level = 0.95)
#집단간 차이가 훨씬크다!! 집단내의차이보다!!
#CEAT-APOLLO 말고모든 브랜드끼리 수명이 다르다



#drug anova분석
#감기약과 피로도의 분석석
drug = read.csv("drug.csv")
drug
str(drug)
drug$fatigue = ordered(drug$fatigue, levels=c("low","med","high"))
boxplot(dose~fatigue, data=drug,
        xlab="fatigue",ylab="dose",
        col = c("blue", "red", "yellow"))

drug.aov = aov(dose~fatigue, data=drug)
summary(drug.aov)

drug.aov02 = update(drug.aov, subset(drug,patientID != 20))
summary(drug.aov02)
plot(drug.aov02)

drug.aov3 = aov(dose~fatigue+gender, data=drug)
summary(drug.aov3)

anova(drug.aov, drug.aov3)
