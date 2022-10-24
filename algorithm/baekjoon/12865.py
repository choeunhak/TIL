# n,k = map(int, input().split())
# weights=[]
# values=[]
# # 가능한 모든 무게를 계산하자!

# result=[]
# for i in range(n):
#     w,v = map(int, input().split())
#     weights.append(w)
#     values.append(v)

# t=0
# while(True):
#     if(t==n):
#         break
#     for i in range(t):
#         if():
#             t=t+1

n, k = map(int, input().split())

thing = [[0,0]]
d = [[0]*(k+1) for _ in range(n+1)]

for i in range(n):
    thing.append(list(map(int, input().split())))

for i in range(1, n+1):
    for j in range(1, k+1):
        print(d)
        w = thing[i][0]
        v = thing[i][1]

        if j < w:
            d[i][j] = d[i-1][j]
        else:
            d[i][j] = max(d[i-1][j], d[i-1][j-w]+v)

print(d[n][k])