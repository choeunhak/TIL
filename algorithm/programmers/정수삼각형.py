#DP -> 정수삼각형


def solution(triangle):
#     for i in range(len(triangle)):
#         triangle[i].append(0)
#         triangle[i].insert(0,0)
        
    
    for i in range(1, len(triangle)):
        for j in range(i+1):
            if(j==0):
                triangle[i][j]=triangle[i][j]+triangle[i-1][j]
            elif(j==len(triangle[i])-1):
                triangle[i][j]=triangle[i][j]+triangle[i-1][j-1]
            else:
                triangle[i][j]=triangle[i][j]+max(triangle[i-1][j], triangle[i-1][j-1])
    answer = max(triangle[len(triangle)-1])
    return answer


triangle=[[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
print(solution(triangle))