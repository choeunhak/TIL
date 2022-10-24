
n=int(input())

def is_han(n):
    strn=str(n)
    diff=0
    if(len(strn)>=2):
        diff=int(strn[1])-int(strn[0])
    for i in range(len(strn)-1):
        if((int(strn[i+1])-int(strn[i]))!=diff):
            return False
    return True

cnt=0
for i in range(n+1):
    if(is_han(i)):
        cnt=cnt+1
print(cnt-1)