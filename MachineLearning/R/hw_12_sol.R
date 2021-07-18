###########################################
# Relationship between Advertising sales and Budgets
###########################################
Advertising=read.csv("ad.csv")
head(Advertising)
summary(Advertising)

#Q1. Is there a relationship between advertising sales and budgets?
#Test hypothesis H0 : beat_TV = beta_radio = beta_newspaper = 0.
ad.lm <- lm(sales~., data=Advertising)
summary(ad.lm)

# F-test indicates clear evidence of a relationship between advertising and sales
# Adjusted R^2 = 0.8951: explain almost 90% of the varian in sales
# Which media contribute to sales?:
# TV and radio are related to sales: the p-values for TV and radio are low
#Is there synergy between the advertising media?

ad.lm2 <- lm(sales~.^2, data=Advertising)
summary(ad.lm2)

#including an interaction term results in a substantial increase in 
# Adjusted R^2 - around 97%
# Prediction
set.seed(1234)
trainingRowIndex <- sample(1:nrow(Advertising), 0.6*nrow(Advertising))
trainingData <- ad[trainingRowIndex, ]
testData <- ad[-trainingRowIndex, ]
m5 <- lm(sales~TV*radio*newspaper, data = trainingData)
summary(m5)
pred <- predict(m5, testData)
actualPred <- data.frame(cbind(actual = testData$sales, pred = pred))
actualPred