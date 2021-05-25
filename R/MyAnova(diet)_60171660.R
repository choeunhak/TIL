#diet 데이터 불러오기기
diet = read.csv("./diet.csv", row.names=1)

#이전의 몸무게에서 6주 후의 몸무게를 빼서 감소한 양의 체중을 나타내는 loss 칼럼 추가
diet$loss = diet$pre.weight - diet$weight6weeks

#anova 분석 및 summary
diet_anova = aov(loss~factor(Diet), data=diet)
summary(diet_anova)
#pvalue가 0.003으로 매우 작은값이다. pvalue는 유의미한 값으로 밝혀졌다.
#따라서 diet 간의 차이가 diet 내의 차이보다 크다.

TukeyHSD(diet_anova)
#diet가 식단유형 3-1, 3-2 사이에 p value가 매우 작은 값으로 유의미한 차이가 있는 것으로 밝혀졌다.
#식단유형 2-1 사이에는 pvalue가 0.05보다 큰 0.91로 유의미한 차이가 없는 것으로 밝혀졌다.