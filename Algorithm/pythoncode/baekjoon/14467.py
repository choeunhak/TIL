n=int(input())

cow={}
cnt=0
for i in range(n):
    num,loc=map(int,input().split())
    if(num in cow):
        if(cow[num]!=loc):
            cnt=cnt+1

    cow[num]=loc

print(cnt)