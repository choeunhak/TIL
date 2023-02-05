# 가로, 세로 또는 대각선 걸어갈 수 있음

from collections import deque

def bfs(graph, c, r, n, m, visited):
    queue=deque()
    queue.append((c,r))
    visited[c][r] = 1
    dx=[-1,1,0,0,1,-1,1,-1]
    dy=[0,0,-1,1,1,-1,-1,1]

    while queue:
        x,y=queue.popleft()
        for i in range(8):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<m and graph[nx][ny]==1 and visited[nx][ny]==0:
                queue.append((nx,ny))
                graph[nx][ny]=graph[x][y]+1
                visited[nx][ny] = 1
    # print("전", visited)

visited = []
while(True):
    w, h = map(int, input().split())
    graph = []
    visited = [[0]*w for _ in range(h)]
    if(w==0 and h==0):
        break
    for i in range(h):
        graph.append(list(map(int, input().split())))

    cnt = 0
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if(graph[i][j]==1 and visited[i][j]==0):
                bfs(graph, i, j, h, w, visited)
                cnt = cnt + 1
                # print("후", visited)

    print(cnt)