n = int(input())
a = list(map(int, input().split()))
increase_dp = [0 for _ in range(n)]
decrease_dp = [0 for _ in range(n)]

for i in range(n):
    for j in range(i):
        if a[i] > a[j] and increase_dp[i] < increase_dp[j]:
            increase_dp[i] = increase_dp[j]
    increase_dp[i] += 1
# print(dp)

for i in range(n-1,-1,-1):
    for j in range(n-1,i,-1):
        if a[i] > a[j] and decrease_dp[i] < decrease_dp[j]:
            decrease_dp[i] = decrease_dp[j]
    decrease_dp[i] += 1

result = [0 for _ in range(n)]
for i in range(n):
    result[i] = increase_dp[i] + decrease_dp[i] -1
print(max(result))