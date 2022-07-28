import math

a,b,v = map(int,input().split())

tmp=v-a
mock=tmp/(a-b)
print(math.ceil(mock)+1)

# 내가 어캐 풀었는지 신기하다
# v-a 말고 v-b로 해주어도 된다.