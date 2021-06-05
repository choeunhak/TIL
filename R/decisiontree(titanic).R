#타이타닉 생존자 예측

titanic=read.csv("titanic_clean.csv", header=TRUE, sep=",")


titanic$pclass=as.factor(titanic$pclass)
titanic$name=as.character(titanic$name)
titanic$ticket=as.character(titanic$ticket)
titanic$cabin=as.character(titanic$cabin)
titanic$survived=factor(titanic$survived, levels=c(0,1))

install.packages("rpart.plot")

library(rpart)
library(rpart.plot)

set.seed(100)
trainingRowIndex=sample(1:nrow(titanic), 0.8*nrow(titanic))
trainingData=titanic[trainingRowIndex,]
testData=titanic[-trainingRowIndex,]

dtl=rpart(survived~pclass+sex+age+sibsp+parch+fare+embarked, data=trainingData)
prp(dtl, type=0, extra=2, digits=4)

#prediction
prediction=predict(dtl, testData, type="class")

#check accuracy
table(ifelse(testData$survived==prediction, "yes", "no"))
