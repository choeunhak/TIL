
install.packages("dplyr")
install.packages("ggplot2")
library(dplyr)
library(ggplot2)

# (1)
plot(mpg$cyl, mpg$hwy, main="cylinder와 고속도로 연비의 관계", xlab="cylinder", ylab="고속도로 연비")
# 두 변수의 관계를 표현해주기 위하여 산포도를 그렸다.
# cylinder가 클수록 고속도로 연비는 낮아진다

# (2)
plot(mpg$cty, mpg$hwy, main="도시 연비에 따른 고속도로 연비의 관계", xlab="도시연비", ylab="고속도로 연비")
# 두 변수의 관계를 표현해주기 위하여 산포도를 그렸다.
# 도시 연비가 클수록 고속도로 연비는 커진다

# (3)
mpg_suv = mpg %>% 
  filter(class=="suv") %>%
  group_by(manufacturer) %>%
  summarise(mean_cty=mean(cty))%>%
  arrange(desc(mean_cty)) %>%
  head(5)

barplot(mpg_suv$mean_cty, main="suv 차종의 도시연비 순위", names.arg=mpg_suv$manufacturer, 
        col=rainbow(5), ylim=(c(0,20)))

# (4)
table(mpg$drv)
mpg_4 = mpg %>%
  filter(drv=="4")
mpg_f = mpg %>%
  filter(drv=="f")
mpg_r = mpg %>%
  filter(drv=="r")

boxplot(mpg_4$hwy, mpg_f$hwy, mpg_r$hwy, col=c("yellow", "cyan", "green"),notch=T,
        names=c("4", "f", "r"), horizontal=TRUE)
# 구동방식에 따른 고속도로 연비의 median값은 f방식이 가장 크고 r방식이 그 다음으로 크고 4방식이 마지막이다.
# r방식의 구동방식이 연비가 가장 퍼져 있다
# f방식의 구동방식은 연비가 이상치들이 높게 5개가 있고 낮게 2개가 있다.
# 세 개 의 구동방식은 신뢰구간이 겹치지 않는다. 따라서 연비는 구동방식에 따라 다르다.