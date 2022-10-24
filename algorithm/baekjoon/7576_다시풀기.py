from collections import deque
def bfs(box, queue):
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<m and box[nx][ny]==0: # 방문 x
                if box[nx][ny]==0: # 0이라면(이동가능)
                    queue.append((nx,ny))
                    box[nx][ny]=box[x][y]+1


m,n=map(int,input().split())
box=[]
for i in range(n):
    box.append(list(map(int,input().split())))

queue=deque()
for c in range(n):
    for r in range(m):
        if(box[c][r]==1):
            queue.append((c,r))

bfs(box, queue)

flag=True
max_value=0
for c in range(n):
    for r in range(m):
        if(box[c][r]==0):
            flag=False
            break
        if(max_value<box[c][r]):
            max_value=box[c][r]

#-1과 0을 어떻게 구분하지?

if(flag==False):
    print(-1)
else:
    print(max_value-1)
