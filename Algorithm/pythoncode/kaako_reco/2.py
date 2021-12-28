def solution(arr, x):
    arr2=[]
    arr3=[]
    for i in range(len(arr)):
        tmp=arr[i]
        while(tmp>=0):
            if(tmp in arr2):
                break
            tmp=tmp-x
        arr2.append(tmp+x)

        tmp=arr[i]
        while(tmp<max(arr)):
            tmp=tmp+x
            if(tmp not in arr3):
                break
        arr3.append(tmp)
    arr4=arr2+arr3
    # print(arr4)
    arr4=sorted(arr4)
    ans=0
    t=0
    for i in range(len(arr4)-1):
        if(t not in arr4):
            ans=t
            break
        elif((arr4[i+1]-arr4[i])>1):
            ans=arr4[i]+1
            break
        else:
            ans=arr4[i]+1
    return ans
        
print(solution([1, 3, 4],2))
print(solution([0, 1, 2, 2, 0, 0, 10, 3],3))
print(solution([0,1,2,2,0,0,10],3))
print(solution([1,1,1,1],2))