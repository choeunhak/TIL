def solution(answers):
    a=[1,2,3,4,5]
    b=[2, 1, 2, 3, 2, 4, 2, 5]
    c=[3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    av=0
    bv=0
    cv=0
    for i in range(len(answers)):
        ai=i%5
        bi=i%8
        ci=i%10
        if(answers[i]==a[ai]):
            av=av+1
        if(answers[i]==b[bi]):
            bv=bv+1
        if(answers[i]==c[ci]):
            cv=cv+1
    answer = []
    t=max(av,bv,cv)
    if(t==av):
        answer.append(1)
    if(t==bv):
        answer.append(2)
    if(t==cv):
        answer.append(3)
    if(len(answer)>1):
        answer.sort()
    return answer