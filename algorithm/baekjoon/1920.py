def binary_search(target, data):
    start = 0
    end = len(data) - 1

    while start <= end:
        mid = (start + end) // 2
        if data[mid] == target:
            return mid # 함수를 끝내버린다.
        elif data[mid] < target:
            start = mid + 1
        else:
            end = mid -1

    return "no"

import sys
# n = int(sys.stdin.readline())

n=int(input())
n_nums =list(map(int,sys.stdin.readline().split()))
n_nums.sort()
m=int(input())
m_nums =list(map(int,sys.stdin.readline().split()))

for i in m_nums:
    if(binary_search(i,n_nums)=="no"):
        print(0)
    else:
        print(1)

# 집합 자료형으로도 풀수 있음