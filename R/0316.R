library(dplyr)
welfare=read.csv("./welfare.csv")


#part1
#1
welfare$gender=ifelse(welfare$gender==1, "male", welfare$gender)
welfare$gender=ifelse(welfare$gender==2, "female", welfare$gender)

#2
welfare$income=ifelse(welfare$income<1, NA, welfare$income)
welfare$income=ifelse(welfare$income>9998, NA, welfare$income)

#3
welfare_nomiss = welfare%>% filter(!is.na(income))
gender_income=welfare_nomiss%>%group_by(gender)%>%summarise(mean_income=mean(income))

#4
ggplot(data=gender_income, aes(x=gender, y = mean_income))+geom_bar(stat="identity")


#part2
#1
welfare$gender=ifelse(welfare$gender==1, "male", welfare$gender)
welfare$gender=ifelse(welfare$gender==2, "female", welfare$gender)

#2
welfare$income=ifelse(welfare$income<1, NA, welfare$income)
welfare$income=ifelse(welfare$income>9998, NA, welfare$income)

#3
welfare_nomiss$age=2021-welfare_nomiss$birth

#3
welfare_nomiss = welfare_nomiss%>% filter(!is.na(income))
age_gender_income=welfare_nomiss%>%group_by(gender,age)%>%summarise(mean_income=mean(income))

#4
ggplot(data=age_gender_income, aes(x=age, y = mean_income, col=gender))+geom_line()