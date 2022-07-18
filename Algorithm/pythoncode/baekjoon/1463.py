# 다시 풀기

# x=int(input())

# dp=[0]*(x+1)

# for i in range(2,x+1):

#     if(i%2==0):
#         dp[i]=dp[i//2]+1
#     if(i%3==0):
#         dp[i]=dp[i//3]+1
#     else:
#         dp[i] = dp[i-1]+1
# print(dp)

# print(dp)

x=int(input())

dp=[0]*(x+1)

for i in range(2,x+1):
    dp[i] = dp[i-1]+1
    if(i%2==0):
        dp[i]=min(dp[i],dp[i//2]+1)
    if(i%3==0):
        dp[i]=min(dp[i],dp[i//3]+1)

print(dp[x])

# if(i%2==0): 이게 elif면 안된다 왜지 ->-1, 2로 나누기, 3으로 나누기 3가지 경우를 다 봐야하기 때문이다
# 따라서 두 if문의 순서가 바껴도 상관이 없다