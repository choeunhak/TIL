#손과 박수의 관계
#운동과 흡연의 관계

library(MASS)
survey

#1
WriteClap=xtabs(~W.Hnd+Clap,data=survey)
chisq.test(WriteClap)
fisher.test(WriteClap)
#카이스퀘어 테스트가 값이 정확하지 않을 수 있기 때문에 fishertest를 사용하였다.
#pvalue가 0.05보다 작기때문에 관계가 있다.
#대립가설을 채택한다.


#교수님 답
#글씨를 쓰는손과 박수칠때 위로가는 손 사이에 관계가 있다


#2
ExerSmoke=xtabs(~Exer+Smoke,data=survey)
ExerSmoke
chisq.test(ExerSmoke)
fisher.test(ExerSmoke)
#카이스퀘어 테스트가 값이 정확하지 않을 수 있기 때문에 fishertest를 사용하였다.
#pvalue가 0.05보다 크기때문에 관계가 없다
#귀무가설을 채택한다.

#교수님 답
#운동과 흡연 사이에 관계가 없다