n,x = map(int, input().split())
num = list(map(int, input().split()))

i=0
cur_sum=0
ans=0
result=[]
for end,val in enumerate(num):
    cur_sum=cur_sum+val
    if(end-i+1==x):
        result.append(cur_sum)
        cur_sum=cur_sum-num[i]
        i=i+1

# print(result)
if(max(result)==0):
    print("SAD")
else:
    print(max(result))
    print(result.count(max(result)))