# 1.   n x r 행, m y c 열

from collections import deque
def bfs(box, c, r):
    queue=deque()
    queue.append((c,r))
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<m and box[nx][ny]==0:
                queue.append((nx,ny))
                box[nx][ny]=box[x][y]+1


m,n=map(int,input().split())
box=[]
for i in range(n):
    box.append(list(map(int,input().split())))

for c in range(n):
    for r in range(m):
        if(box[c][r]==1):
            bfs(box, c,r)
            # print(visited)
# visited[0][0]=0

print(box)
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


#참조 https://jae04099.tistory.com/entry/%EB%B0%B1%EC%A4%80-7576-%ED%86%A0%EB%A7%88%ED%86%A0-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%95%B4%EC%84%A4%ED%8F%AC%ED%95%A8