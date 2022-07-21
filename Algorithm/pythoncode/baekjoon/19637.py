
import sys
input = sys.stdin.readline
n, m = map(int, input().split())
level=[]
fight=[]

def binary_search(target, data):
    data.sort()
    start = 0
    end = len(data)-1

    while start <= end:
        mid = (start + end) // 2
        # print(data)


        # if data[mid] == target:
        #     return mid # 함수를 끝내버린다.
        if data[mid] < target:
            start = mid + 1
        else:
            end = mid -1
        print("start", start)
        print("end", end)
        print("mid", mid)

    return start

for i in range(n):
    l, f = map(str, input().split())
    level.append(l)
    fight.append(int(f))

for i in range(m):
    tmp=int(input())
    idx = binary_search(tmp, fight)
    print(level[idx])

