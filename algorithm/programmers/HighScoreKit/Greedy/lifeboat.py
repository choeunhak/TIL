def solution(people, limit):
    sort_peo = sorted(people)
    i=len(people)-1
    answer = 0
    while(sort_peo):
        max_peo = sort_peo[i]
        
        print(sort_peo)
        print(max_peo)
        print()
        if(max_peo+sort_peo[0]<=100):
            sort_peo.remove(sort_peo[0])
            sort_peo.remove(max_peo)
        else:
            sort_peo.remove(max_peo)
        i=i-1
        answer=answer+1
        if(not sort_peo):
            break
    return answer
print(solution([70, 80, 50], 100))
#limit에 가장 가깝게 만들어야한다!
#1. 정렬시킨다
#2. 100에서 최댓값을 뺀다
#3. 그 수가 있으면 최댓값과 그수를 리스트에서 뺀다
# 없으면 최댓값+최솟값이 100안넘으면 리스트에서 뺀다
# 100을 넘으면 그냥 뺀다
#4. 언제까지? -> limit의 절반이 될때까지 
#나머지 수들은 그냥 더하면된다

#https://leedakyeong.tistory.com/entry/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-%EA%B5%AC%EB%AA%85%EB%B3%B4%ED%8A%B8-in-python