from collections import deque

def solution(queue1, queue2):
    deq1=deque(queue1)
    deq2=deque(queue2)
    sum_deq1 = sum(deq1)
    sum_deq2 = sum(deq2)
    length = len(queue1) + len(queue2)
    cnt=0
    while(True):
        if(sum_deq1==sum_deq2):
            break
        # if(not deq1 or not deq2):
        #     cnt=-1
        #     break
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
        if(cnt>length and sum_deq1 != sum_deq2):
            return -1
        cnt=cnt+1

    return cnt

print(solution([3, 2, 7, 2], [4,6,5,1]))