from collections import deque

m,n,h=map(int,input().split())
box=[]
for j in range(h):
    tmp=[]
    for i in range(n):
        tmp.append(list(map(int,input().split())))
    box.append(tmp)

def bfs(box):
    dx=[-1,1,0,0,0,0]
    dy=[0,0,-1,1,0,0]
    dz=[0,0,0,0,-1,1]
    while queue:
        z,x,y=queue.popleft()
        for i in range(6):
            nx,ny,nz=x+dx[i],y+dy[i],z+dz[i]
            # print(nz,nx,ny)
            if 0<=nx<n and 0<=ny<m and 0<=nz<h and box[nz][nx][ny]==0:
                queue.append((nz,nx,ny))
                box[nz][nx][ny]=box[z][x][y]+1
queue=deque()
for t in range(h):
    for r in range(n):
        for c in range(m):
            if(box[t][r][c]==1):
                queue.append((t,r,c))

bfs(box)


flag=True
max_val=-2
for t in range(h):
    for r in range(n):
        for c in range(m):
            if(box[t][r][c]==0):
                flag=False
                break
            if(box[t][r][c]>=max_val):
                max_val=box[t][r][c]

if(flag==False):
    print(-1)
else:
    print(max_val-1)

# 아래 필요없음
# elif(max_val==-1):
#     print(0)




# 1.   n x r 행, m y c 열

# 2. bfs 돌리기전에 큐에다가 넣고 돌리는게 맞는듯!
# if(box[t][r][c]==1):
#   queue.append((t,r,c))
# 이부분!
