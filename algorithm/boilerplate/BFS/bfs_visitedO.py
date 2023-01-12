from collections import deque

def bfs(graph, c, r, color, visited):
    queue=deque()
    queue.append((c,r))
    visited[c][r] = 1
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<n and graph[nx][ny]==color and visited[nx][ny]==0:
                queue.append((nx,ny))
                visited[nx][ny] = 1

n = int(input())
area = [list(str(input())) for _ in range(n)]
visited = [[0]*n for _ in range(n)]
disable_visited = [[0]*n for _ in range(n)]

normal_cnt = 0
disable_cnt = 0

for i in range(n):
    for j in range(n):
        if(visited[i][j]==0):
            bfs(area, i, j, area[i][j], visited)
            normal_cnt = normal_cnt+1

print(normal_cnt, disable_cnt)
