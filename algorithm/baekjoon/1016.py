mi, ma = map(int, input().split())

visited = [False]*(ma-mi+1)
answer = ma-mi+1

for i in range(2,int(ma**0.5+1)):
    square = i**2
    for j in range((((mi-1)//square)+1)*square, ma+1, square):
        if(visited[j-mi]==False):
            visited[j-mi] = True
            answer=answer-1


print(answer)