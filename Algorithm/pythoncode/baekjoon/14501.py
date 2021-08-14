
n = 7

t_list = [3,5,1,1,2,4,2]
p_list = [10,20,10,20,15,40,200]
dp = [0,0,0,0,0,0,0,0,0,0,0]

for i in range(n):
    print("i:",i)
    print("dp", dp)
    if dp[i] > dp[i + 1]:
        print("다음날 받게 될 금액 : dp[i+1]", dp[i+1])
        print("(큰금액)현재 받게 될 금액 : dp[i]", dp[i])
        dp[i + 1] = dp[i]
    if dp[i + t_list[i]] < dp[i] + p_list[i]:
        print("현재 금액 : dp[i + t_list[i]]", dp[i + t_list[i]])
        print("(큰금액)i일 뒤에 받게 될 금액 dp[i] + p_list[i]", dp[i] + p_list[i])
        dp[i + t_list[i]] = dp[i] + p_list[i]

print(dp[n])


