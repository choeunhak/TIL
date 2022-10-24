def solution(numbers):
    answer = []
    i=0
    while(i<len(numbers)):
        j=i+1
        while(j<len(numbers)):
            answer.append(numbers[i]+numbers[j])
            j=j+1
        i=i+1
    answer=set(answer)
    answer=list(answer)
    answer.sort()
    return answer
print(solution([2,1,3,4,1]))