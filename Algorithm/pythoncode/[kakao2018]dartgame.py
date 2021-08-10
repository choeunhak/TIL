#다트게임

dartResult="1S2D*3T"
dartResult2="1D2S#10S2"
def solution(dartResult):
    score=[]
    for i in range(11):
        score.append(str(i))
    answer = 0
    for i in range(len(dartResult)):
        print("answer", answer)
        past=0
        temp=0
        if(dartResult[i] in score):
            past=temp
            temp=dartResult[i]
        if(dartResult[i]=='S'):
            answer=answer+(int(temp))^1
        elif(dartResult[i]=='D'):
            answer=answer+(int(temp))^2
        elif(dartResult[i]=='T'):
            answer=answer+(int(temp))^3

        if(dartResult[i]=='*'):
            answer=answer+(int(temp))*2
        elif(dartResult[i]=='#'):
            answer=answer+(int(temp))^-1
    return answer

print(solution(dartResult))
# print(solution(dartResult2))