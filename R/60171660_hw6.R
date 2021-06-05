library(openxlsx)
df<-read.xlsx("sidoAirInfo.xlsx",sheet=1,startRow=2)

city=c()
pm=c()
register_google(key="")

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
