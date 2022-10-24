def solution(brown, yellow):
    # 노랑 소인수분해가 아니라 두 수의 곱으로 모두 표현
    i=1
    tmp=[]
    while(i<=int(yellow)):
        if(yellow%i==0):
            tmp.append([i,int(yellow/i)])
        i=i+1
    answer = []
    # 두수의 곱으로 표현 후에 brown 공식 적용
    for t in tmp:
        if(t[0]+t[1]+1 == brown/2-1):
            answer = t
            
    
    # 그럼 그 때의 yellow 값에서 전체 가로 세로를 추출할수 있따!
    answer[0]=answer[0]+2
    answer[1]=answer[1]+2
    return answer

# brown + yellow = 가로 * 세로
# 가로 >= 세로