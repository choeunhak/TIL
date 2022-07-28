import math

a,b,v = map(int,input().split())

tmp=v-a
mock=tmp/(a-b)
print(math.ceil(mock)+1)