#BFS 단지번호붙이기

import sys
from collections import deque
input=sys.stdin.readline

n=int(input())
maze=[list(map(int,list(input().rstrip()))) for _ in range(n)]

# maze = [[0, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0, 1], [1, 1, 1, 0, 1, 0, 1], [0, 0, 0, 0, 1, 1, 1], [0, 1, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0, 0]]
visited= [[0]*n for _ in range(n)]

dx=[-1,1,0,0]
dy=[0,0,-1,1]

queue=deque()
def bfs(x,y):
    queue.append((x,y))
    visited[x][y] = 1
    size=1
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            # print(nx,ny)
            # print('m',maze[nx][ny])
            # print('v',visited[nx][ny])
            if 0<=nx<n and 0<=ny<n and visited[nx][ny]==0: # 방문 x
                if maze[nx][ny]==1: # maze에서 1이라면(이동가능)
                    queue.append((nx,ny))
                    size=size+1
                    visited[nx][ny]=1 # 방문 비용 +1
    return size

result=[]
for i in range(n):
    for j in range(n):
        # 현재 위치에서 BFS 수행
        if maze[i][j]==1 and visited[i][j]==0:
            result.append(bfs(i,j))
result.sort()
print(len(result))
for i in range(len(result)):
    print(result[i])