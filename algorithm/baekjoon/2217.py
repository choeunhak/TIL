import sys
input = sys.stdin.readline

n = int(input())
ropes = []

for i in range(n):
    ropes.append(int(input()))

ropes.sort()
answer = 0
for i in range(n):
    tmp = (n-i)*ropes[i]
    answer = max(answer, tmp)

print(answer)