n=int(input())

def fact(n):
    if(n==1):
        return 1
    else:
        return n*fact(n-1)

if(n==0):
    res=1
else:
    res=fact(n)

print(res)