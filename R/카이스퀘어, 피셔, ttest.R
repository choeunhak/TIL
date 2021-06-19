library(MASS)
data("survey")
str(survey)
SexExer = xtabs(~Sex+Exer, data=survey)
SexExer
addmargins(SexExer)
chisq.test(SexExer)

#chisq
child1 = c(5,11,1)
child2 = c(4,7,3)
Toy = cbind(child1,child2)
rownames(Toy) = c("car", "truck", "doll")
Toy
chisq.test(Toy)

#fisher
fisher.test(Toy) 

#KS검정
x = rnorm(50)
y = runif(30)
ks.test(x, y)

#Shapiro Wilk Test
shapiro.test(rnorm(100,mean=5,sd=3))

#cfb::UsingR
library(UsingR)
str(cfb)
shapiro.test(cfb$INCOME)
hist(cfb$INCOME, breaks=100)
hist(cfb$INCOME, freq=FALSE, breaks=100,
     main = "Kernel Density Plot of cfb$INCOME")

qqnorm(cfb$INCOME)
qqline(cfb$INCOME)


#T-test
t.test(x, y=NULL, alternative = c("two.sided","less","greater"),
       mu=0,
       paired = FALSE,
       var.equal = FALSE,
       conf.level = 0.95)

#사례1 표본이 하나인 경우
a = c(980, 1008, 968, 1032, 1012, 996, 1021, 1002, 996, 1017)
shapiro.test(a)
t.test(a, mu=1000, alternative = "two.sided")

#사례2 표본이 하나인 경우
b = c(58,49,39,99,32,88,62,30,55,65,44,55,57,53,88,42,39)
shapiro.test(b)#정규분포 검사
t.test(b, mu=55, alternative = "greater")

#사례3표본이 두개인 경우
pre = c(13.2, 8.2, 10.9, 14.3, 10.7, 6.6, 9.5, 10.8, 8.8, 13.3)
post = c(14.0, 8.8, 11.2, 14.2, 11.8, 6.4, 9.8, 11.3, 9.3, 13.6)
shapiro.test(pre)
shapiro.test(post)
var.test(pre,post)
t.test(pre,post, paired = FALSE, var.equal = TRUE)

#귀무가설: 차이가없다(평균이같다다)

#사례4 표본이 두개인 경우(정규분포하지않아 wilcox 수행)
A = c(rep(5,8), rep(4,11), rep(3,9), rep(2,2), rep(1,3))
A
B = c(rep(5,4), rep(4,6), rep(3,10), rep(2,8), rep(1,4))
B

shapiro.test(A)
shapiro.test(B)
wilcox.test(A,B,exact = F, correct = F)

#paired는 관련된 집단인지 아닌지에 따라 달라지는듯
#일반적으론 false

#paired t-test: 독립적이지 않은 집단, 즉, 사전/사후 검사의 평균 차이가 유의한지 볼 때. 
#unpaired t-test (=독립표본t test?): 독립적인 두개의 집단 간의 평균 차이가 유의한지 볼 때

#ttest실습
str(sleep)
data = sleep
sleep2 = sleep[,-3]
tapply(sleep2$extra, sleep2$group, mean)

var.test(extra~group, sleep2)
t.test(extra~group, data = sleep2, paired=FALSE, var.equal=TRUE)
with(sleep, t.test(extra[group==1], extra[group==2], paired=TRUE))