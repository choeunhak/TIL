def solution(scoville, K):
    #가장 작은 지수를 뺀다
    #두번째로 작은 지수를 뺀다
    # 스코빌 지수 계산해서 다시 넣는다
    #정렬한다
    answer = 0
    while(True):
        if(min(scoville)>=K):
            break
        scoville.sort()
        try:
            most_min = scoville.pop(0)
            second_min = scoville.pop(0)
            newValue = most_min+(second_min*2)
            scoville.insert(1,newValue)
            # if(scoville[0]<newValue):
            #     scoville.insert(1,newValue)
            # else:
            #     scoville.insert(1,newValue)
        except IndexError:
            return -1
        answer=answer+1
    return answer