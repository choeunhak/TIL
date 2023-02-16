n = int(input())
k = int(input())
board = [([0]*n) for _ in range(n)]

for i in range(k):
    c,r = map(int, input().split())
    board[c-1][r-1] = 'a'

l = int(input())
dirs = []
for i in range(l):
    dir = list(map(str, input().split()))
    dirs.append(dir)

dx = [0,0,-1,1]
dy = [1,-1,0,0]

x = 0
y = 0

# 오른쪽 이동
# X초가 끝난 뒤에 왼쪽(C가 'L') 또는 오른쪽(C가 'D')로 90도 방향 회전
while(True):
    if()