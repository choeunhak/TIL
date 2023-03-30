import copy
from collections import deque
dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)

def dfs(graph, r, c, chance):
    global MAX, visited
    MAX = max(MAX, visited[r][c])
    for d in range(4):
        nr = r + dr[d]
        nc = c + dc[d]
        if not (0 <= nr < n and 0 <= nc < n) or visited[nr][nc]:
            continue
        if graph[r][c] > graph[nr][nc]:
            visited[nr][nc] = visited[r][c] + 1
            dfs(nr, nc, chance)
            visited[nr][nc] = 0
        elif chance and graph[nr][nc] - K < graph[r][c]:
            temp = graph[nr][nc]
            graph[nr][nc] = graph[r][c] - 1
            visited[nr][nc] = visited[r][c] + 1
            dfs(nr, nc, chance-1)
            visited[nr][nc] = 0
            graph[nr][nc] = temp


T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    n, k = map(int, input().split())
    maps = [list(map(int, input().split())) for _ in range(n)]
    # print(maps)
    MAX = 0
    # k를 0~k까지 모든 점에 적용시켜가면서
    # 각 경우의 최대 길이를 구한다!
    for t in range(k+1):
        for i in range(n):
            for j in range(n):
                tmp_copy = copy.deepcopy(maps)
                tmp_copy[i][j] = tmp_copy[i][j] - t
                for r in range(n):
                    for c in range(n):
                        dfs(tmp_copy, r, c, 1)
    print(MAX)

## 틀림.. BFS로는 안됨...




# 10
# 5 1
# 9 3 2 3 2
# 6 3 1 7 5
# 3 4 8 9 9
# 2 3 7 7 7
# 7 6 5 5 8