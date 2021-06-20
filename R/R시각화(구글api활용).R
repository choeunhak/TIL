library(openxlsx)
#https://www.weather.go.kr/w/index.do 여기서 지진엑셀파일 다운로드
df<-read.xlsx("sidoAirInfo.xlsx",sheet=1,startRow=2)

#지도데이터 전처리
df[,6] = gsub("N","",df[,6]) #위도 숫자 뒤 "N"제거
df[,7] = gsub("E","",df[,7]) #경도 숫자 뒤 "E"제거
df2 = data.frame(lon=df[,7], lat=df[,6], mag=df[,3])
df2[,1]=as.numeric(as.character(df2[,1]))
df2[,2]=as.numeric(as.character(df2[,2]))
df2[,3]=as.numeric(as.character(df2[,3]))


city=c()
pm=c()
register_google(key="A")#구글api입력

i=2
while(i<ncol(df)){
  city[i-1]=df[1,i]
  pm[i-1]=df[2,i]
  i=i+1
}

gc=data.frame()
p=1
while(p<ncol(df)-1){
  temp=geocode(enc2utf8(city[p]))
  gc=rbind(gc,temp)
  p=p+1
}

data=data.frame(city=city, pm=pm, lon=gc$lon, lat=gc$lat)
data$pm=as.numeric(data$pm)

library(ggplot2)

#Q1
ggplot(data=data, aes(x=reorder(city,-pm), y=pm))+geom_col()


library(ggmap)


cen=c((max(df2$lon)+min(df2$lon))/2,
      (max(df2$lat)+min(df2$lat))/2)

map=get_googlemap(center=cen, zoom=6)
gmap=ggmap(map)

#Q2
gmap+geom_point(data=data,aes(x=lon,y=lat), color="red", size=data$pm/4,alpha=0.5)
