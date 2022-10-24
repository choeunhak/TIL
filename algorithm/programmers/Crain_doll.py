#크레인인형뽑기게임
#https://programmers.co.kr/learn/courses/30/lessons/64061?language=python3
#sol1
board=[[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,3],[0,2,5,0,1],[4,2,4,4,2],[3,5,1,3,1]]
moves=[1,5,3,5,1,2,1,4]

def solution(board, moves):
    answer = 0
    box=[]
    for m in range(len(moves)):
        for i in range(len(board)):
            if(board[i][moves[m]-1]!=0):
                box.append(board[i][moves[m]-1])
                board[i][moves[m]-1]=0
                
                if(len(box)>1):
                    if(box[-1]==box[-2]):
                        del box[-1]
                        del box[-1]
                        answer=answer+2
                break
    return answer
print(solution(board,moves))