def solution(brown, yellow):
    sum = brown + yellow
    divisor = []
    answer = []
    
    for i in range(1,sum+1):
        if sum%i==0:
            divisor.append(i)
            
    mid = len(divisor)//2 - 1
    
    print(divisor)
    if sum%2==0:
        answer.append(divisor[mid])
        answer.append(divisor[mid+1])
    else:
        answer.append(divisor[mid+1])
        answer.append(divisor[mid+1])
        
    answer.sort(reverse=True)

    return answer

print(solution(2002,998))