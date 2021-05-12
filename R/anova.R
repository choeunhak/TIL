tyre=read.csv("./tyre.csv")

library(dplyr)

#기본통계량표
tyre%>%group_by(Brands)%>%
  summarise(N=n(), Mean=mean(Mileage), Median=median(Mileage), Min=min(Mileage),
                                               Max=max(Mileage), SD=sd(Mileage))
#boxplot 생성
boxplot(tyre$Mileage~tyre$Brands,
        col=rainbow(4),
        horizontal=TRUE)

#브랜드별로 타이어의 수명이 다른디 아노바를 사용하여 분석
tyres.aov=aov(Mileage~Brands,tyre)
summary(tyres.aov)
#Fvalue가 17.9, Pvalue가 매우작은값으로 타이어브랜드별로 수명이 다르다

#어떤 브랜드끼리 다를까?
TukeyHSD(tyres.aov, conf.level = 0.95)
#CEAT-APOLLO 말고모든 브랜드끼리 수명이 다르다
