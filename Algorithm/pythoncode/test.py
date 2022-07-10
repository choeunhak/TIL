def solution(arr):
    answer=[]
    for i in range(len(arr)-1):
        print("i",arr[i])
        print("i+1",arr[i+1])
        if(arr[i+1]!=arr[i]):
            answer.append(arr[i+1])
    return answer
print(solution([1,1,1,4,4,4,4,4,8,7,7]))