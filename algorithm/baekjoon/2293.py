# n, k = map(int, input().split())
# coins = []
# for i in range(n):
#     coins.append(int(input()))

# print(coins)

# DP 어렵다...
n, k = map(int, input().split())
c = [int(input()) for i in range(n)] # 코인의 종류
dp = [0 for i in range(k+1)] # 사이즈 k+1만큼의 리스트 선언
dp[0] = 1 # 인덱스 0은 동전을 1개만 쓸 때의 경우의 수를 고려하기 위해 선언

for i in c:

    for j in range(i, k+1):
        # print(i,j)

        if j-i >= 0:
            dp[j] = dp[j] + dp[j-i]
    # print(dp)


print(dp[k])

# 이 생각을 어캐하지?