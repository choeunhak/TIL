# 예제 입력 3에서 틀림
# 2 2 0 0 16
# 0 2
# 3 4
# 4 4 4 4 1 1 1 1 3 3 3 3 2 2 2 2

# 핵심 포인트 : 주사위가 동서남북으로 이동했을 때 칸이 어떻게 이동하는지 아니?

def roll_dice(dir):
    east, west, south, north, above, down = dice[0], dice[1], dice[2], dice[3], dice[4], dice[5]
    # 동쪽
    if(dir == 1):
        dice[0], dice[1], dice[4], dice[5] = down, above, east, west

    # 서쪽
    elif(dir == 2):
        dice[0], dice[1], dice[4], dice[5] = above, down, west, east

    # 북쪽
    elif(dir == 3):
        dice[2], dice[3], dice[4], dice[5] = above, down, north, south

    # 남쪽
    elif(dir == 4):
        dice[2], dice[3], dice[4], dice[5] = down, above, south, north

n, m, x, y, k = map(int, input().split())
dice = [0]*6

maps = []
for i in range(n):
    row = list(map(int, input().split()))
    maps.append(row)

instructions = list(map(int, input().split()))

dx = [0,0,0,-1,1]
dy = [0,1,-1,0,0]

nx = x
ny = y

for i in instructions:

    if(nx+dx[i] < 0 or nx+dx[i] >= n or ny + dy[i] < 0 or ny + dy[i] >= m):
        continue
    else:
        nx = nx + dx[i]
        ny = ny + dy[i]

    # print("후", nx,ny)

    roll_dice(i)

    # 칸에 숫자 0이면 -> 바닥면 숫자 칸에 복사
    # 0이 아니면 칸에 숫자가 바닥면에 복사, 칸에 숫자 0
    if(maps[nx][ny]==0):
        maps[nx][ny] = dice[5]
    else:
        dice[5] = maps[nx][ny]
        maps[nx][ny] = 0

    print(dice[4])
