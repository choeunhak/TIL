from collections import deque

n = int(input())
area = []
for i in range(n):
  area.append(list(map(int, input().split())))

max_val = 0
for i in range(n):
  for j in range(n):
    if (area[i][j] > max_val):
      max_val = area[i][j]

safe_area = []

visited = [[False for _ in range(n)] for _ in range(n)]


def bfs(c, r, t):
  global visited
  queue = deque()
  queue.append((c, r))
  dx = [-1, 1, 0, 0]
  dy = [0, 0, -1, 1]
  while queue:
    x, y = queue.popleft()
    for i in range(4):
      nx, ny = x + dx[i], y + dy[i]
      if 0 <= nx < n and 0 <= ny < n and area[nx][ny] > t and not visited[nx][
          ny]:
        visited[nx][ny] = True
        queue.append((nx, ny))


# bfs(0,0,2)
for t in range(max_val):
  cnt = 0
  for i in range(n):
    for j in range(n):
      if (not visited[i][j] and area[i][j] > t):
        visited[i][j] = True
        bfs(i, j, t)
        cnt = cnt + 1
  safe_area.append(cnt)
  visited = [[False for _ in range(n)] for _ in range(n)]

print(max(safe_area))
