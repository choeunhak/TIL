#2021 인턴 거리두기
#13:45~

from collections import deque

# 1. 파티션 허용이 있으면 2여도 허용(대각선, 2칸)
# 2. 거리가 2이고 파티션 없으면 거리두기 안지킨거

#결과 10111
# def check
places=[["POOOP", "OXXOX", "OPXPX", "OOXOX", "POXXP"], ["POOPX", "OXPXP", "PXXXO", "OXXXO", "OOOPP"], ["PXOPX", "OXOXP", "OXPOX", "OXXOP", "PXPOX"], ["OOOXX", "XOOOX", "OOOXX", "OXOOX", "OOOOO"], ["PXPXP", "XPXPX", "PXPXP", "XPXPX", "PXPXP"]]


# 이동할 네 가지 방향 정의 (상, 하, 좌, 우)
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# BFS 소스코드 구현
def bfs(z, x, y):
    # 큐(Queue) 구현을 위해 deque 라이브러리 사용
    flag=0
    queue = deque()
    queue.append((x, y))
    check = [[0]*5 for _ in range(len(places[0]))]
    distance = [[0]*5 for _ in range(len(places[0]))]
    print(distance)
    check[x][y]=1
    # 큐가 빌 때까지 반복하기
    while queue:
        x, y = queue.popleft()
        # 현재 위치에서 4가지 방향으로의 위치 확인
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            # 공간을 벗어난 경우 무시
            if (0 <= nx < 5) and (0 <= ny < 5) and (not check[nx][ny]):
            # 벽인 경우 무시
                if places[z][nx][ny] == "0":
                    queue.append((nx, ny))
                    check[nx][ny]=1
                    distance[nx][ny] = distance[x][y]+1
                if places[z][nx][ny] == "P" and distance[x][y]<=1:
                    return 0
    # 가장 오른쪽 아래까지의 최단 거리 반환
    return 1

def solution(places):
    answer = []
    for i in range(len(places)): 
        flag=1
        for j in range(len(places[i])):
            for k in range(len(places[i][j])):
                if(places[i][j][k]=="P"):
                    flag=bfs(i,j,k)
        answer.append(flag)
    return answer

print(solution(places))