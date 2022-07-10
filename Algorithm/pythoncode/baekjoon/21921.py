n,x = map(int, input().split())
num = list(map(int, input().split()))

result=[]
for i in range(len(num)):
    result.append(sum(num[i:i+x]))

if(max(result)==0):
    print("SAD")
else:
    print(max(result))
    print(result.count(max(result)))