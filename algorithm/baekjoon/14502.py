# deepcopy안쓰고는 못푸나..?

n, m = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(n)]

from collections import deque
from itertools import combinations
import copy
def bfs(graph, c, r):
    queue=deque()
    queue.append((c,r))
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            if 0<=nx<n and 0<=ny<m and graph[nx][ny]==0 and (graph[nx][ny]!=1):
                queue.append((nx,ny))
                # 여기서 graph 바꿔주면 안되는데....
                graph[nx][ny]=2

zero_area = []

# 0 전체 위치 구하기
for i in range(n):
    for j in range(m):
        if(graph[i][j]==0):
            zero_area.append([i,j])

# 3개 고르기
tmp_wall_area = list(combinations(zero_area,3))
# print(tmp_wall_area)

tmp_safe_area = []

# 벽 세우고 안전영역 세기
for t in range(len(tmp_wall_area)):
    zero_cnt = 0
    tmp_graph = copy.deepcopy(graph)
    tmp_graph[tmp_wall_area[t][0][0]][tmp_wall_area[t][0][1]]=1
    tmp_graph[tmp_wall_area[t][1][0]][tmp_wall_area[t][1][1]]=1
    tmp_graph[tmp_wall_area[t][2][0]][tmp_wall_area[t][2][1]]=1
    for i in range(n):
        for j in range(m):
            if(tmp_graph[i][j]==2):
                bfs(tmp_graph, i, j)
    for i in range(n):
        for j in range(m):
            if(tmp_graph[i][j]==0):
                zero_cnt = zero_cnt+1
    tmp_safe_area.append(zero_cnt)

print(max(tmp_safe_area))