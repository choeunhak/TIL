import sys
from collections import deque

input = sys.stdin.readline

def D(arr):
    if(len(arr)==0):
        return "error"
    # 뒤에서 하나 제거
    if(arr[0]=="R"):
        arr.pop()
        return arr
    # 앞에서 하나 제거
    else:
        arr.popleft()
        return arr

def R(arr):
    if(len(arr)==0):
        return deque()
    if(arr[0]=="R"):
        arr.popleft()
        return arr
    else:
        arr.appendleft("R")
        return arr


t = int(input())
for _ in range(t):
    p = str(input())
    n = int(input())
    arr = deque(input().rstrip()[1:-1].split(","))
    if n == 0:
        arr = deque()
    for i in range(len(p)):
        if(p[i]=="R"):
            arr = R(arr)
        elif(p[i]=="D"):
            arr = D(arr)
            if(arr=="error"):
                break
    if(arr=="error"):
        print("error")
    elif(arr[0]=="R"):
        arr.popleft()
        arr.reverse()
        arr = list(arr)
        print("["+",".join(arr)+"]")
    else:
        print("["+",".join(arr)+"]")
