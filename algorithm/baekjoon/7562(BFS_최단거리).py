t = int(input())

from collections import deque

def bfs(graph, visited, start_x, start_y):
    queue=deque()
    queue.append((start_x, start_y))
    dx=[1,2,2,1,-1,-2,-2,-1]
    dy=[2,1,-1,-2,2,1,-1,-2]

    while queue:
        x,y=queue.popleft()

        for i in range(8):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<len(graph) and 0<=ny<len(graph) and visited[nx][ny]==0:
                queue.append((nx,ny))
                visited[nx][ny] = visited[x][y] + 1

visited = []
for _ in range(t):
    i = int(input())
    graph = [[1]*i for _ in range(i)]
    visited = [[0]*i for _ in range(i)]

    start_x, start_y =  map(int, input().split())
    end_x, end_y =  map(int, input().split())
    if(start_x == end_x and start_y == end_y):
        print(0)
    else:
        bfs(graph, visited, start_x, start_y)
        print(visited[end_x][end_y])
