import heapq
import sys

input = sys.stdin.readline
n = int(input())
heap = []
for i in range(n):
    x = int(input())
    if(x==0):
        # 원소 삭제
        if(heap):
            print(heapq.heappop(heap))
        else:
            print(0)
    else:
        # 원소 추가
        heapq.heappush(heap, x)


# 최소힙