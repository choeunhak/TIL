n=int(input())
nums=list(map(int,input().split()))

dp=[0]*n
for i in range(len(nums)):
    print(dp)
    dp[i]=max(nums[i],nums[i]+dp[i-1])

print(max(dp))