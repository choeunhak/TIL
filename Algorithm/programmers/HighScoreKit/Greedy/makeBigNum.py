def solution(number, k):
    answer = ''
    while(k>0):
        print(k)
        for i in range(len(number)-1):
            if(number[i]<number[i+1]):
                number=number[0:i]+number[i+1:]
                k=k-1
                break
            elif(i==len(number)-2):
                number=number[0:len(number)-k]
                k=0
                break
    answer=number
    return answer
print(solution("54321",2))