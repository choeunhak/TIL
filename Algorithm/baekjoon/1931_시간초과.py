n=int(input())
time=[]
for i in range(n):
    start, end = map(int, input().split())
    time.append([start,end])

time.sort()
# print(time)

for i in range(len(time)):
    for j in range(i,len(time)):
        # print("end", time[i][-1])
        # print("start", time[j][-2])
        if(time[i][-1]<=time[j][0]):
            # print(time)
            time[i]=time[i]+time[j]
            # break

max_val=0
for i in range(len(time)):
    if(len(time[i])>=max_val):
        max_val=len(time[i])
print(max_val//2)