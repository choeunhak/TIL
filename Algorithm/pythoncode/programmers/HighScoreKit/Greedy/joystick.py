from string import ascii_uppercase

alp = list(ascii_uppercase)

print(alp)

def solution(name):
    tmp=['A']*len(name)
    rev_alp = list(ascii_uppercase)
    name=list(name)
    rev_alp.reverse()
    print(rev_alp)
    answer = 0
    i=0
    while(True):
        print(tmp)
        print(name)
        if(tmp==name):
            break
        # print(abs(alp.index(tmp[i])-alp.index(name[i])))
        # print(abs(alp.index(name[i])-alp.index(tmp[i])))
        cnt = min(abs(alp.index(tmp[i])-alp.index(name[i])),abs(alp.index(name[i])-rev_alp.index(tmp[i])))
        answer=answer+cnt
        tmp[i]=name[i]
        #왼, 오 비교 위치 찾는 과정'
        for t in range(int(len(name)/2)+1):
            print(i)
            print(t)
            if(tmp[i-t]!=name[i-t]):
                i=i-t
                break
            elif(tmp[i+t]!=name[i+t]):
                i=i+t
                break
        answer=answer+1
        print(answer)
    return answer
print(solution("JEROEN"))