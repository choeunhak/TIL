import math

n=str(input())
cnt=[0]*9
for i in n:
    if(i=="9"):
        cnt[int(6)]=cnt[int(6)]+1
    else:
        cnt[int(i)]=cnt[int(i)]+1
cnt[int(6)]=math.ceil(cnt[int(6)]/2)

print(max(cnt))