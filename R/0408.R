library(dplyr)
mpg%>%select(model)

mpg

mpg_suv = mpg %>% 
  filter(class=="suv") %>%
  group_by(manufacturer) %>%
  summarise(mean_cty=mean(cty))%>%
  arrange(desc(mean_cty)) %>%
  head(5)

mpg_suv

#이렇게만 하면 그냥 알파벳순으로 정렬됨됨
ggplot(data=mpg_suv, aes(x=manufacturer, y=mean_cty))+geom_col()
#ggplot에서의 정렬, -는 내림차순으로 해달라는의미임임
ggplot(data=mpg_suv, aes(x=reorder(manufacturer,-mean_cty), y=mean_cty))+geom_col()


barplot(mpg_suv$mean_cty, main="suv 차종의 도시연비 순위", names.arg=mpg_suv$manufacturer, 
        col=rainbow(5), ylim=(c(0,20)))

