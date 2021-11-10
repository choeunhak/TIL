n=int(input())
tri=[]
ans=[]

for i in range(n):
    tmp=input().split()
    tmp.insert(0,'0')
    tmp.append('0')
    tri.append(tmp)
ans.append(tri[0])
for i in range(1, len(tri)):
    tmpans=[0]
    for j in range(1, len(tri[i])-1):
        tmpValue=max(int(ans[i-1][j-1]), int(ans[i-1][j]))+int(tri[i][j])
        tmpans.append(max(int(ans[i-1][j-1]), int(ans[i-1][j]))+int(tri[i][j]))
    tmpans.append(0)
    ans.append(tmpans)

print(max(ans[n-1]))
# [0,0,1,0,1,2,0,2,3,2,3,4,3,0,3]
# [4]