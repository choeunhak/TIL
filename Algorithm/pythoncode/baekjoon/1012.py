from collections import deque

def bfs(farm, visited, c, r):
    queue=deque()
    queue.append((c,r))
    visited[c][r]=0
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<m and 0<=ny<n and visited[nx][ny]==-1: # 방문 x
                if farm[nx][ny]==1: # 1이라면(이동가능)
                    visited[nx][ny]=0 # 방문 비용 0
                    queue.append((nx,ny))

t=int(input())
result=[]
for i in range(t):
    m,n,k=map(int,input().split())
    farm=[[0]*n for _ in range(m)]

    #1로 표시하기
    for i in range(k):
        x,y=map(int, input().split())
        farm[x][y]=1
    visited= [[-1]*n for _ in range(m)]
    #시작점 무조건 넣지 않기
    cnt=0
    for c in range(m):
        for r in range(n):
            if(farm[c][r]==1 and visited[c][r]==-1):
                bfs(farm, visited, c, r)
                cnt=cnt+1
    print(cnt)

