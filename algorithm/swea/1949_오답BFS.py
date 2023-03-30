import copy
from collections import deque
answer = []
def bfs(graph, c, r):
    print(graph, graph[c][r])
    visited = [[0]*n for _ in range(n)]
    length = [[0]*n for _ in range(n)]
    queue=deque()
    queue.append((c,r))
    visited[c][r] = 1
    dx=[-1,1,0,0]
    dy=[0,0,-1,1]
    while queue:
        x,y=queue.popleft()
        for i in range(4):
            nx,ny=x+dx[i],y+dy[i]
            if 0<nx<n-1 and 0<ny<n-1 and visited[nx][ny]==0:
                visited[nx][ny] = visited[nx][ny] + 1
                queue.append((nx,ny))
                if(graph[nx][ny] <= graph[x][y]):
                    length[nx][ny] = max(length[nx][ny], length[nx-1][ny], length[nx][ny-1], length[nx+1][ny], length[nx][ny+1])+1
        # print(visited)
    print(length)
    answer.append(max(max(length)))


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    n, k = map(int, input().split())
    maps = [list(map(int, input().split())) for _ in range(n)]
    # print(maps)

    # k를 0~k까지 모든 점에 적용시켜가면서
    # 각 경우의 최대 길이를 구한다!
    for t in range(k+1):
        for i in range(n):
            for j in range(n):
                tmp_copy = copy.deepcopy(maps)
                tmp_copy[i][j] = tmp_copy[i][j] - t
                for r in range(n):
                    for c in range(n):
                        bfs(tmp_copy, c, r)
    print(max(answer))

## 틀림.. BFS로는 안됨...




# 10
# 5 1
# 9 3 2 3 2
# 6 3 1 7 5
# 3 4 8 9 9
# 2 3 7 7 7
# 7 6 5 5 8