n,k = map(int, input().split())

coins =[]
for i in range(n):
    coin=int(input())
    coins.append(coin)


i=len(coins)-1
cnt=0
while(True):
    if(k==0):
        break
    if(coins[i]<=k):
        mock=k//coins[i]
        cnt=cnt+mock
        k=k-mock*coins[i]
        # print(k)
    if(i==0):
        break
    i=i-1

print(cnt)