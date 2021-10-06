weights=[50,82,75,120]
head2head=["NLWL","WNLL","LWNW","WWLN"]
def solution(weights, head2head):
    result=[]
    answer = []
    for i in range(len(head2head)):
        N=0
        L=0
        W=0
        cnt=0
        for j in range(len(head2head[i])):
            if(head2head[i][j]=="N"):
                N=N+1
            elif(head2head[i][j]=="L"):
                L=L+1
            elif(head2head[i][j]=="W"):
                W=W+1
                if (weights[i] < weights[j]):
                    cnt += 1
        if (W+L != 0):
            result.append([i+1, W/(W+L), cnt, weights[i]])
        else:
            result.append([i+1, 0, cnt, weights[i]])
    result.sort(reverse=True, key = lambda x : (x[1],x[2],x[3]) )
    for i in range(len(result)):
        answer.append(result[i][0])
    return answer


print(solution(weights, head2head))