library(dplyr)

mtcars

help(mtcars)

disp_gear_aov <- aov(mtcars$disp~factor(mtcars$gear))
summary(disp_gear_aov)
#pvalue가 2.56e-06로 매우 작은값이다. pvalue는 유의미한 값으로 밝혀졌다.
#따라서 gear 그룹 간의 차이가 gear 그룹 내의 차이보다 크다.

TukeyHSD(disp_gear_aov)
#gear가 4-3, 5-3 사이에 p value가 매우 작은 값으로 유의미한 차이가 있는 것으로 밝혀졌다.
#5-4 사이에는 pvalue가 0.05보다 큰 0.18로 유의미한 차이가 없는 것으로 밝혀졌다.