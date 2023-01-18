import sys

input  = sys.stdin.readline

n=int(input())
nums=list(map(int, input().split()))

dp = [1]*n
for i in range(1,n):
    print(dp)
        # 앞에서 현재값보다 작으면서, 가장 큰값을 찾아야함.
    tmp_max_index = 0
    for j in range(i-1,0,-1):
        if(nums[j]<nums[i] and nums[tmp_max_index]<nums[j]):
            tmp_max_index = j
    # print(tmp_max_index)
    # if(nums[i]<nums[tmp_max_index]):
    if(nums[tmp_max_index] < nums[i]):
        dp[i]=dp[tmp_max_index]+1

print(max(dp))

# 이전의 최댓값을 어떻게 알지?
