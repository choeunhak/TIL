mi, ma = map(int, input().split())

visited = [False]*(ma-mi+1)
answer = ma-mi+1

for i in range(2,int(ma**0.5+1)):
    square = i**2
    # 제곱수만 골라서 answer에서 빼주면 되기 때문에 square만큼 증가함
    for j in range((((mi-1)//square)+1)*square, ma+1, square):
        if(visited[j-mi]==False):
            visited[j-mi] = True
            # 제곱ㄴㄴ수
            answer=answer-1


print(answer)