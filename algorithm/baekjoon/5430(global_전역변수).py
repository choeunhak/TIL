import sys
from collections import deque

input = sys.stdin.readline
isR = 0
def D(arr):
    if(len(arr)==0):
        return "error"
    # 뒤에서 하나 제거
    # print("??",isR)
    if(isR==1):
        arr.pop()
        return arr
    # 앞에서 하나 제거
    else:
        arr.popleft()
        return arr

def R():
    global isR
    if(isR==1):
        isR=0
    else:
        isR=1

t = int(input())
for _ in range(t):
    p = str(input())
    n = int(input())
    isR = 0
    arr = deque(input().rstrip()[1:-1].split(","))
    if n == 0:
        arr = deque()
    for i in range(len(p)):
        if(p[i]=="R"):
            R()
        elif(p[i]=="D"):
            arr = D(arr)
            if(arr=="error"):
                break
    if(arr=="error"):
        print("error")
    elif(isR==1):
        arr.reverse()
        arr = list(arr)
        print("["+",".join(arr)+"]")
    else:
        print("["+",".join(arr)+"]")
