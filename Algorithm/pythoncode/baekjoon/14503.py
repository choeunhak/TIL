n,m = map(int, input().split())
r,c,d = map(int,input().split())
graph=[]
visited= [[0]*m for _ in range(n)]

for i in range(n):
    graph.append(list(map(int,input().split())))

result=0

def clean(r,c):
    while(True):
        if(visited[r-1][c]==1 and visited[r+1][c]==1 and visited[r][c-1]==1 and visited[r][c+1]==1 and graph[r-1][c]==1):
            break
        if(visited[r][c]==0):
            visited[r][c]=1
            result=result+1
    


clean(r,c)