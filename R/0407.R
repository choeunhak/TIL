s1=c(100,100,49)
s2=c(100,100,100)
s3=c(50,50,50)
score=data.frame(s1,s2,s3)





pass_fail=function(score){
  result=c()
  for(i in 1:nrow(score)){
    if(score[i,1]<50 | score[i,2]<50 | score[i,3]<50){
      result[i]="fail"}
    else{
      result[i]="pass"}
    cat(i, '번째 학생은', result[i], '입니다\n')}
}



result=pass_fail(score)

print(3)


kk=read.csv("./R/burger.csv")


plot(10:1)


close.screen(all=True)

split.screen(c(2,1))
split.screen(c(1,3))
