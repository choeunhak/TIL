t = int(input())
n = []
for _ in range(t):
    n.append(list(map(int, input().split())))
for i in range(1, t):
    for j in range(len(n[i])):
        if(j==0):#맨처음
            n[i][j] += n[i-1][j]
        elif (i==j): #맨끝
            n[i][j] += n[i-1][j-1]
        else:
            n[i][j]+=max(int(n[i-1][j-1]), int(n[i-1][j]))

print(max(n[t-1]))
# [0,0,1,0,1,2,0,2,3,2,3,4,3,0,3]
# [4]