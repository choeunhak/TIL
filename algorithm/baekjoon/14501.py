
n = int(input())
t_list = []
p_list = []
dp = [0] * (n+5)
for i in range(n):
    tmp = input().split()
    t_list.append(int(tmp[0]))
    p_list.append(int(tmp[1]))

for i in range(n):
    print(i)
    print("전", dp)
    if dp[i] > dp[i + 1]:
        dp[i + 1] = dp[i]
    if dp[i + t_list[i]] < dp[i] + p_list[i]:
        dp[i + t_list[i]] = dp[i] + p_list[i]
    print("후", dp)
print(dp)


