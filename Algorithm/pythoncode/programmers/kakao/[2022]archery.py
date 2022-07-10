def calcPoint(apeach, lion):
    apeach_score = 0
    lion_score = 0
    for i in range(11):
        if apeach[i] == lion[i] == 0:
            continue
        if apeach[i] >= lion[i]:
            apeach_score += 10 - i
        else:
            lion_score += 10 - i
    return lion_score - apeach_score

# 지금쏘는 과녁 idx, 남은 화살 개수, 어피치점수, 내점수
def DFS(idx, n, apeach, lion):
    print(apeach)
    print(lion)
    global answer, point
    if n < 0:
        return
    #점수 계산
    if idx > 10:
        diff = calcPoint(apeach, lion)
        if diff <= 0:
            return
        if diff > point:
            point = diff
            answer = [lion[i] for i in range(11)]
            answer[10] += n            
        return

    #상대가 쏜 점수보다 높이 쏴본다
    lion[10-idx] = apeach[10-idx]+1
    DFS(idx+1, n-lion[10-idx], apeach, lion)
    
    lion[10-idx] = 0
    DFS(idx+1, n, apeach, lion)

def solution(n, info):
    global answer, point
    answer = [-1]
    point = 0
    DFS(0, n, info, [0 for _ in range(11)])
    return answer


print(solution(5, [2,1,1,1,0,0,0,0,0,0,0]))