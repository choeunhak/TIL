n,k = map(int,input().split())
coins=[]

for i in range(n):
    coins.append(int(input()))

i=len(coins)
i=i-1
cnt=0
while(True):
    if(k==0):
        break
    if(k//coins[i]==0):
        cnt=cnt+1
        k=k-k//coins[i]
    i=i-1

print(cnt)