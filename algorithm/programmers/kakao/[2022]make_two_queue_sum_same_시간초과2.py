from collections import deque

def solution(queue1, queue2):

    queue12 = queue1+queue2
    deq1=deque(queue1)
    deq2=deque(queue2)

    cnt=0
    while(True):
        if(sum(deq1)==sum(deq2)):
            break
        if(len(deq1)==len(queue12) or len(deq1)==len(queue12)):
            cnt=-1
            break
        elif(sum(deq1)>sum(deq2)):
            tmp = deq1.popleft()
            deq2.append(tmp)
        elif(sum(deq2)>sum(deq1)):
            tmp = deq2.popleft()
            deq1.append(tmp)
        cnt=cnt+1

    return cnt

print(solution([3, 2, 7, 2], [4,6,5,1]))