n=int(input())
a=list(map(int,input().split()))
b=list(map(int,input().split()))

result=[]

tmp=0

a.sort()
b.sort(reverse=True)
for j in range(len(b)):
    tmp=tmp+a[j]*b[j]
# while(True):
#     if(i==n):
#         break
#     for j in range(len(b)):
#         tmp=tmp+a[cnt]*b[j]
#     i=i+1
#     result.append(tmp)
#     print(tmp)

print(tmp)