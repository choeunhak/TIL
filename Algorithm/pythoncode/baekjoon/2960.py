n,k = map(int, input().split())

nums=[False,False]+[True]*(n-1)

cnt=0
flag=False
for i in range(2,n+1):
    if(flag==True):
        break
    for j in range(i,n+1,i):
        if(nums[j]==True):
            # print(j)
            nums[j]=False
            cnt=cnt+1

        if(cnt==k):
            print(j)
            flag=True
            break
