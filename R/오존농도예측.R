#오존농도예측

# Compute monthly mean in Ozone
for (i in 1:nrow(airquality)){
  if(is.na(airquality[i,"Ozone"])){
    airquality[i,"Ozone"]<- mean(airquality[which(airquality[,"Month"]==airquality[i,"Month"]),"Ozone"],na.rm = TRUE)
  }
  # Compute monthly mean in Solar.R
  if(is.na(airquality[i,"Solar.R"])){
    airquality[i,"Solar.R"]<- mean(airquality[which(airquality[,"Month"]==airquality[i,"Month"]),"Solar.R"],na.rm = TRUE)
  }
}

Solar=airquality[,"Solar.R"]
Wind=airquality[,"Wind"]
Temp=airquality[,"Temp"]
Ozone=airquality[,"Ozone"]

#선형모델
m1 = lm(Ozone~Solar*Wind*I(Temp^2))
summary(m1)

#Solar와 Wind와 제곱으로 가중치를 Temp가 영향을 주고 동시에 상호작용하여 영향을 줄 때 
#adjusted r-squared값이 0.5743으로
#Ozone 농도를 예측하는 최상의 선형회귀 모델이 나오는 것으로 예측된다.

