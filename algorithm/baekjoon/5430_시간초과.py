import sys
input = sys.stdin.readline

def D(arr):
    if(len(arr)==2):
        return "error"
    # 뒤에서 하나 제거
    if(arr[0]=="D"):
        i = len(arr)-1
        while(True):
            if(arr[i]==","):
                break
            i=i-1
        return arr[:i]+"]"
    # 앞에서 하나 제거
    else:
        i = 0
        while(True):
            if(i==len(arr)):
                break
            if(arr[i]==","):
                break
            i=i+1
        if(i<len(arr)):
            return "["+arr[i+1:]
        else:
            return "[]"

def R(arr):
    if(arr[0]=="D"):
        return arr[1:]
    else:
        return "D"+arr


t = int(input())
for _ in range(t):
    p = str(input())
    n = int(input())
    arr = str(input())
    for i in range(len(p)):
        if(p[i]=="R"):
            arr = R(arr)
        elif(p[i]=="D"):
            arr = D(arr)
    if(arr=="error"):
        print("error")
    elif(arr[0]=="D"):
        print("[", end="")
        for i in range(len(arr)-2,1,-1):
            print(arr[i], end="")
        print("]")
    else:
        print(arr)
