#60171660 조은학
#Part1-1

#이상치로 income이 9999이상 0인 수치 제외
wel=read.csv("./welfare.csv")

library(dplyr)
wel$income=ifelse(wel$income<1, NA, wel$income)
wel$income=ifelse(wel$income>9998, NA, wel$income)

#NA제거
wel_nomiss = wel%>% filter(!is.na(income))

wel_nomiss$age=2021-wel_nomiss$birth

wel_nomiss=wel_nomiss%>%mutate(age_group=ifelse(wel_nomiss$age<30,'young', 
       ifelse(wel_nomiss$age>=60, 'old', 'middle')))

wel_ageincome=wel_nomiss%>%group_by(age_group)%>%summarise(mean_income=mean(income))

library(ggplot2)
ggplot(data=wel_ageincome, aes(x=age_group, y=mean_income))+geom_col()
#중년 연령대의 평균 income이 가장 많다.



#Part1-2

Code_Name=data.frame(code_region=c(1,2,3,4,5,6,7), region_name=c("서울", "광주/전남/전북/제주도", "수도권(인천/경기)", 
                                                                 "부산/경남/울산", "대구/경북", "대전/충남",
                                                                 "강원/충북"))
wel_nomiss = wel%>% filter(!is.na(income))
wel_nomiss_region=left_join(wel_nomiss, Code_Name, id="code_region")
wel_nomiss_region=wel_nomiss_region%>%group_by(region_name)%>%summarise(mean_income=mean(income))

ggplot(data=wel_nomiss_region, aes(x=mean_income, y=reorder(region_name, mean_income)))+geom_col()
#대구/경북 지역의 평균 income이 가장 많다.



#Part2-3
replacena=function(x){
  ifelse(is.na(x), mean(x,na.rm=T),x)
}

x=c(7,12,9,15,NA,8,14,2,9,NA,8)
replacena(x)

#Part3-4
B=c(57,78,42,44,91,65,63,60,97,85,92,42,64,81,64)
G=c(73,96,74,55,91,50,46,82,43,79,79,50,46,81,83)

boxplot(B,G, col=c("yellow", "green"), names=c("남학생", "여학생"), horizontal=TRUE)
#여학생의 상위 25~75프로 사이의 분포가 남학생의 상위 25~75의 분포보다 넓다. 
#남학생의 중앙값이 여학생의 중앙값보다 낮다.
#상위 25프로의 값은 남학생이 여학생보다 높다.
#상위 75프로의 값은 남학생이 여학생보다 높다.