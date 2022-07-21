from collections import deque
import copy
def bfs(box, c, r):
    # cnt=[[-1]*m for _ in range(n)]
    cnt = copy.deepcopy(box)
    queue=deque()
    queue.append((c,r))
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<m and cnt[nx][ny]==0: # 방문 x
                if box[nx][ny]==0: # 0이라면(이동가능)
                    queue.append((nx,ny))
                    # visited[nx][ny]=visited[x][y]+1
                    cnt[nx][ny]=cnt[x][y]+1


    return cnt


m,n=map(int,input().split())
box=[]
for i in range(n):
    box.append(list(map(int,input().split())))

tmp=0
pre=[]
for c in range(n):
    for r in range(m):
        if(box[c][r]==1):
            tmp = bfs(box, c,r)
            if(pre):
                for c in range(n):
                    for r in range(m):
                        tmp[c][r]=min(tmp[c][r],pre[c][r])
            pre = copy.deepcopy(tmp)
            # print(visited)
# visited[0][0]=0

# print(tmp)
flag=True
max_value=0
for c in range(n):
    for r in range(m):
        if(tmp[c][r]==0):
            flag=False
            break
        if(max_value<tmp[c][r]):
            max_value=tmp[c][r]

#-1과 0을 어떻게 구분하지?

if(flag==False):
    print(-1)
else:
    print(max_value-1)
