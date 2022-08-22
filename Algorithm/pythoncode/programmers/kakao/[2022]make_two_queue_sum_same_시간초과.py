from collections import deque

def solution(queue1, queue2):
    queue12 = queue1+queue2
    deq1=deque(queue1)
    deq2=deque(queue2)
    sum_deq1 = sum(deq1)
    sum_deq2 = sum(deq2)
    cnt=0
    while(True):
        if(sum_deq1==sum_deq2):
            break
        if(len(deq1)==len(queue12) or len(deq1)==len(queue12)):
            cnt=-1
            break
        elif(sum_deq1>sum_deq2):
            tmp = deq1.popleft()
            deq2.append(tmp)
            sum_deq1 = sum_deq1-tmp
            sum_deq2 = sum_deq2+tmp
        elif(sum_deq2>sum_deq1):
            tmp = deq2.popleft()
            deq1.append(tmp)
            sum_deq2 = sum_deq2-tmp
            sum_deq1 = sum_deq1+tmp
        cnt=cnt+1

    return cnt

print(solution([3, 2, 7, 2], [4,6,5,1]))