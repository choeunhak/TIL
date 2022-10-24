def solution(n):
    temp=""
    while(True):
        if(n==0):
            break
        temp=temp+str(n%3)
        n=n//3
        
    i=len(temp)
    result=0
    t=0
    while(i>0):
        result=result+int(temp[i-1])*3**t
        i=i-1
        t=t+1
    answer = result
    return answer

print(solution(45))