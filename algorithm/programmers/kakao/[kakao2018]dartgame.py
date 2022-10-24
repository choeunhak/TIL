#다트게임
dartResult="1S*2T*3S"
def solution(dartResult):
    score=[]
    for i in range(11):
        score.append(str(i))
    answer = []
    i=0
    while(i<len(dartResult)):
        if(i<len(dartResult)-1):
            if((dartResult[i]+dartResult[i+1]) in score):
                answer.append(int(dartResult[i]+dartResult[i+1]))
                i=i+1
            elif(dartResult[i] in score):
                answer.append(int(dartResult[i]))
        if(dartResult[i]=='S'):
            answer[-1]=answer[-1]**1
        elif(dartResult[i]=='D'):
            answer[-1]=answer[-1]**2
        elif(dartResult[i]=='T'):
            answer[-1]=answer[-1]**3

        if(dartResult[i]=='*'):
            if(len(answer)!=1):
                answer[-2]=answer[-2]*2
            answer[-1]=answer[-1]*2
        elif(dartResult[i]=='#'):
            answer[-1]=answer[-1]*-1
        i=i+1
    return sum(answer)

print(solution(dartResult))
# print(solution(dartResult2))