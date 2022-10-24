from collections import deque

def bfs(p):
    start = []
    
    for i in range(5): # 시작점이 되는 P 좌표 구하기
        for j in range(5):
            if p[i][j] == 'P':
                start.append([i, j])
    
    for s in start:
        queue = deque([s])  # 큐에 초기값
        visited = [[0]*5 for i in range(5)]   # 방문 처리 리스트
        distance = [[0]*5 for i in range(5)]  # 경로 길이 리스트
        visited[s[0]][s[1]] = 1
        
        while queue:
            x, y = queue.popleft()
        
            dx = [-1, 1, 0, 0]  # 좌우
            dy = [0, 0, -1, 1]  # 상하
            print(distance)
            print(p)
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]

                if 0<=nx<5 and 0<=ny<5 and visited[nx][ny] == 0:
                    
                    #빈테이블이기 때문에 탐색이 가능해서 큐에 추가한다
                    if p[nx][ny] == 'O':
                        queue.append([nx, ny])
                        visited[nx][ny] = 1
                        distance[nx][ny] = distance[x][y] + 1
                    
                    if p[nx][ny] == 'P' and distance[x][y] <= 1:
                        return 0
    return 1

places=[["POOOP", "OXXOX", "OPXPX", "OOXOX", "POXXP"], ["POOPX", "OXPXP", "PXXXO", "OXXXO", "OOOPP"], ["PXOPX", "OXOXP", "OXPOX", "OXXOP", "PXPOX"], ["OOOXX", "XOOOX", "OOOXX", "OXOOX", "OOOOO"], ["PXPXP", "XPXPX", "PXPXP", "XPXPX", "PXPXP"]]
def solution(places):
    answer = []
    
    for i in places:
        answer.append(bfs(i))
    
    return answer
solution(places)