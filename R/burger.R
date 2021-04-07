#60171660 조은학

#1
brand=c('M', 'L', 'B')
Menu=c("빅맥", "불고기버거", "치즈와퍼")
Kcal=c('514', '533', '566')
Na=c('917', '817', '920')
Fat=c('15', '13', '12')


burger=data.frame(brand=brand, Menu=Menu, Kcal=Kcal, Na=Na, Fat=Fat)
burger

#2-1
burger[1,4]
#2-2
burger$Kcal
#2-3
burger[c(1,3),"Menu"]