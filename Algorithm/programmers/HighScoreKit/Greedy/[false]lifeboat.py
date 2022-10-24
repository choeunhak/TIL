
import math
def solution(people, limit):
    sort_peo = sorted(people)
    i=len(people)-1
    answer = 0
    while(True):
        if(sort_peo[i]<=limit/2):
            break
        max_peo = sort_peo[i]
        tmp=100-max_peo
        if(tmp in sort_peo):
            sort_peo.remove(tmp)
            sort_peo.remove(max_peo)
        elif(max_peo+tmp<100):
            sort_peo.remove(tmp)
            sort_peo.remove(max_peo)
        else:
            sort_peo.remove(max_peo)
        i=i-1
        answer=answer+1
    answer=answer+math.ceil(len(sort_peo)/2)
    return answer
#limit에 가장 가깝게 만들어야한다!
#1. 정렬시킨다
#2. 100에서 최댓값을 뺀다
#3. 그 수가 있으면 최댓값과 그수를 리스트에서 뺀다
# 없으면 최댓값+최솟값이 100안넘으면 리스트에서 뺀다
# 100을 넘으면 그냥 뺀다
#4. 언제까지? -> limit의 절반이 될때까지 
#나머지 수들은 그냥 더하면된다