n=int(input())
time=[]
for i in range(n):
    start, end = map(int, input().split())
    time.append([start,end])

time = sorted(time, key=lambda a: a[0])
time = sorted(time, key=lambda a: a[1])

# cnt=0
# last=0
# for i,j in time:
#     if(i>=last):
#         cnt=cnt+1
#         last=j

# print(cnt)
cnt=0
last=1

for i in range(len(time)):
    if(last<=time[i][0]):
        cnt=cnt+1
        last=time[i][-1]
print(cnt)