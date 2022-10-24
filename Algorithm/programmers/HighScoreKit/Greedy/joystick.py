from string import ascii_uppercase

alp = list(ascii_uppercase)

def solution(name):
    tmp=['A']*len(name)
    rev_alp = list(ascii_uppercase)
    name=list(name)
    rev_alp.reverse()
    answer = 0
    i=0
    while(True):
        
        cnt = min(abs(alp.index(tmp[i])-alp.index(name[i])),abs(alp.index(name[i])-rev_alp.index(tmp[i]))+1)
        print("cnt", cnt)
        answer=answer+cnt
        tmp[i]=name[i]
        # 왼, 오 비교 위치 찾는 과정'
        for t in range(int(len(name)/2)+1):
            if(i-t>=-len(name) and i+t<len(name)):
                if(tmp[i+t]!=name[i+t]):
                    i=i+t
                    answer=answer+t
                    break
                elif(tmp[i-t]!=name[i-t]):
                    i=i-t
                    answer=answer+t
                    break
                

        if(tmp==name):
            break
        
    return answer
print(solution("JEROEN"))
print(solution("JAZ"))