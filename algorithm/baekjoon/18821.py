n = int(input())
graph = []
for _ in range(n):
    graph.append(list(map(int, input().split())))

def get_distance(a,b,c,d):
    return ((a-c)**2+(b-d)**2)**(1/2)

# print(get_distance(2,2,0,0))


prof = []
sung = []
answer = 0
for i in range(n):
    for j in range(n):
        if(graph[i][j]==5):
            prof = [i,j]
        elif(graph[i][j]==2):
            sung = [i,j]


cnt = 0

start_x = min(sung[0], prof[0])
start_y = min(sung[1], prof[1])
end_x = max(sung[0], prof[0])
end_y = max(sung[1], prof[1])
for i in range(start_x, end_x+1):
    for j in range(start_y, end_y+1):
        if(graph[i][j]==1):
            cnt=cnt+1

if(get_distance(prof[0], prof[1], sung[0], sung[1])>=5 and cnt >=3):
    answer = 1

print(answer)