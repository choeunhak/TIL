n=int(input())
costs=[]
for i in range(n):
    costs.append(list(map(int,input().split())))

for i in range(1, len(costs)):
    for j in range(3):
        costs[i][j]=costs[i][j]+min(costs[i-1][j-1],costs[i-1][j-2])


print(min(costs[len(costs)-1]))