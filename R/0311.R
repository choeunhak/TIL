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
