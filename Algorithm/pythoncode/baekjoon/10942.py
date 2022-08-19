n=int(input())
nums=list(map(int,input().split()))
ques=int(input())

dp = [[0 for _ in range(n)] for _ in range(n)]

for i in range(n):
    for s in range(n-i):
        e=s+i
        if(s==e):
            dp[s][e]=1
        elif(nums[s]==nums[e]):
            # print(nums[s:e+1])
            if(s+1==e):
                dp[s][e]=1
            elif(dp[s+1][e-1]==1):
                dp[s][e]=1

for i in range(ques):
    s, e = map(int, input().split())
    print(dp[s-1][e-1])