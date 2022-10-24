n=int(input())
stair=[0]
for i in range(n):
    stair.append(int(input()))

dp=[0]*(n+1)


k=n-1
dp[k]=stair[k]
k=k-1

while(True):
    print(dp)
    if(k<0):
        break
    dp[k]=max(stair[k-1]+stair[k-2], stair[k-2]+stair[k-3], stair[k-1]+stair[k-3])
    k=k-3

print(sum(dp))
# def walk(a):

