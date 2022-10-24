n=int(input())
m=int(input())

d_check = [False for _ in range(n + 1)]

edge = [[] for _ in range(n + 1)]

# for _ in range(m):
#     v1, v2 = map(int, input().split())
#     edge[v1].append(v2)
#     edge[v2].append(v1)
 
# for e in edge:
#     e.sort()
    
edge = [[], [2, 5], [1, 3, 5], [2], [7], [1, 2, 6], [5], [4]]

print(edge)
virus=[]
def dfs(x):
    d_check[x] = True
    virus.append(x)
    print(d_check)
    for y in edge[x]:
        if d_check[y] == False:
            dfs(y)
dfs(1)
print(len(virus)-1)