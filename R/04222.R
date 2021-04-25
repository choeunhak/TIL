B=c(57,78,42,44,91,65,63,60,97,85,92,42,64,81,64)
G=c(73,96,74,55,91,50,46,82,43,79,79,50,46,81,83)

boxplot(B,G, col=c("yellow", "green"), names=c("남학생", "여학생"), horizontal=TRUE)
#여학생의 상위 25~75프로 사이의 분포가 남학생의 상위 25~75의 분포보다 넓다. 
#남학생의 중앙값이 여학생의 중앙값보다 낮다.
#상위 25프로의 값은 남학생이 여학생보다 높다.
#상위 75프로의 값은 남학생이 여학생보다 높다.

print(#)
print(3)  

print(3)


install.packages("ggplot2")
install.packages("dplyr")

library(ggplot2)
library(dplyr)


#Q1
displ4 = mpg %>% filter(displ<=4)
displ5 = mpg %>% filter(displ>=5)

mean(displ4$hwy)
mean(displ5$hwy)



#Q2

US = mpg %>% filter(manufacturer=="chevrolet" | manufacturer== "dodge" | manufacturer== "ford" | manufacturer== "lincoln")
Japan = mpg %>% filter(manufacturer=="honda" | manufacturer== "nissan" | manufacturer== "subaru" | manufacturer== "toyota")

mean((US$cty+US$hwy)/2)
mean((Japan$cty+Japan$hwy)/2)


#Q3

mpg %>% mutate(avg_mpg=(cty+hwy)/2) %>% arrange(desc(avg_mpg)) %>%head(1) %>% select(manufacturer, model, avg_mpg)

plot(10:1)

split.screen(c(2,1))
split.screen(1)
screen(1)
plot(1:10)
