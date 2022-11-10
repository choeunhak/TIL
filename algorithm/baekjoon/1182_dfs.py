from sys import stdin

input = stdin.readline

array = []
N, S = map(int, input().split())
array = list(map(int, input().split()))

s = []
cnt = 0
def dfs(start):
    global cnt
    if len(s) > 0 and sum(s) == S:
        cnt += 1

    for i in range(start, N):
        s.append(array[i])
        dfs(i+1)
        s.pop()

dfs(0)
print(cnt)
