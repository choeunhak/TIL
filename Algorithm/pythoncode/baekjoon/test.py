# 맞는 풀이
n, k = map(int, input().split())

thing = [[0,0]]
dp = [[0]*(k+1) for _ in range(n+1)]

for i in range(n):
    thing.append(list(map(int, input().split())))

for i in range(1, n+1):
    print(dp)
    for j in range(1, k+1):
        w = thing[i][0]
        v = thing[i][1]

				# 1. 현재 배낭의 허용 무게보다 넣을 물건의 무게가 더 크다면 넣지 않는다.
        if j < w:
            dp[i][j] = dp[i-1][j]
				# 2. max(현재 넣을 물건의 무게만큼 배낭에서 빼고 현재 물건을 넣기, 현재 물건을 넣지않고 이전 배낭 그대로)
        else:
            dp[i][j] = max(dp[i-1][j-w]+v, dp[i-1][j])

print(dp[n][k])