
import sys
n = int(input())
lines = []
for i in range(n):
    lines.append(int(sys.stdin.readline()))

# print(lines)

lines.sort(reverse = True)
answer = -1
# print(lines)
for i in range(len(lines)-2):
    if(lines[i]<(lines[i+1]+lines[i+2])):
        answer =lines[i]+lines[i+1]+lines[i+2]
        break

print(answer)