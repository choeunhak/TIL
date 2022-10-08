n = int(input())
levels=[]
for i in range(n):
    levels.append(int(input()))

max_val=0
# for i in range(levels[n-1]-n+1, levels[n-1]+1):
#     max_val=max_val+i


i=len(levels)-1
cnt=0
while(True):
    # print(levels)
    if(i<=0):
        break
    if(levels[i-1]<levels[i]):
        pass
    else:
        cnt=cnt+levels[i-1]-levels[i]+1
        levels[i-1]=levels[i]-1
    i=i-1
print(cnt)
