#BOJ 1926
#도화지!!!
#BFS로 풀어보자!

from collections import deque

N, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(n)]
# N,M = 6,5
# graph = [[1, 1, 0, 1, 1], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [1, 0, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 1, 1, 1]]

area_list=[]

# N, M을 공백을 기준으로 구분하여 입력 받기
# N, M = map(int, input().split())
# # # 2차원 리스트의 맵 정보 입력 받기
# graph = []
# for i in range(N):
#     graph.append(list(map(int, input().split())))
    
check = [[0]*M for _ in range(N)]

# 이동할 네 가지 방향 정의 (상, 하, 좌, 우)
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# BFS 소스코드 구현
def bfs(x, y):
    # 큐(Queue) 구현을 위해 deque 라이브러리 사용
    size=1
    queue = deque()
    queue.append((x, y))
    # 큐가 빌 때까지 반복하기
    while queue:
        x, y = queue.popleft()
        # 현재 위치에서 4가지 방향으로의 위치 확인
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            # 공간을 벗어난 경우 무시
            if (0 <= nx < N) and (0 <= ny < M):
            # 벽인 경우 무시
                if graph[nx][ny] == 1 and not check[nx][ny]:
                    size=size+1
                    check[nx][ny]=1
                    queue.append((nx, ny))
    # 가장 오른쪽 아래까지의 최단 거리 반환
    return size

# BFS를 수행한 결과 출력
result = 0
for i in range(N):
    for j in range(M):
        # 현재 위치에서 DFS 수행
        if graph[i][j]==1 and not check[i][j]:
            result=result+1
            check[i][j] = 1
            area_list.append(bfs(i,j))
            
print(len(area_list))
print(max(area_list))