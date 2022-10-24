def solution(seoul):
    i=0
    while(True):
        if(seoul[i]=="Kim"):
            break
        i=i+1
    answer = "김서방은 "+str(i)+"에 있다"
    return answer

print(solution(["Jane", "Kim"]))