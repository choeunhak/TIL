install.packages("ggplot2")
library(ggplot2)

ggplot(data=economics, aes(x=date, y=unemploy))+geom_line()

help("economics")

economics

qplot(age, circumference, data=Orange, geom="line", colour=Tree, main="asdg")
qplot(Sepal.Length,Petal.Length, data=iris,color=Species,size=Petal.Width, alpha=0.2)
#서로다른 색깔, 서로 다른 점크기, alpha는 점크기


install.packages("ggmap")
library(ggmap)


map=get_googlemap(center=c(126.975684,37.572752))
map=get_googlemap(center=c(126.975684,37.572752), maptype="roadmap", zoom=17, size=c(320,320))
ggmap(map, extent="device")
#여백이 없는상태태

#geocode로 지역명 찾을수있다..?

gc=geocode(enc2utf8("가락래미안"))
gc

lonlat=c(gc
$lon,gc$lat)
lonlat
map=get_googlemap(center=lonlat, maptype="roadmap", zoom=13, size=c(320,320),marker=gc)
ggmap(map)

#개신기하네...
install.packages("openxlsx")
library(openxlsx)
df<-read.xlsx("earthqu.xlsx",sheet=1,startRow=4)


head(df)
df[,6]=gsub("N", "",df[,6])#N제거
df[,7]=gsub("E", "",df[,7])#E제거거

df2=data.frame(lon=df[,7],lat=df[,6],mag=df[,3])#위도,경도, 규모만떼기기
str(df2)

#숫자로 바꿔야함
df2[,1]=as.numeric(as.character(df2[,1]))
df2[,2]=as.numeric(as.character(df2[,2]))
df2[,3]=as.numeric(as.character(df2[,3]))
str(df2)

