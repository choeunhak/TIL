t=int(input())

for i in range(t):
    n=int(input())
    dp=[1, 1, 1, 2, 2]+[0]*n
    for j in range(4,n):
        dp[j]=dp[j-2]+dp[j-3]
    print(dp[n-1])