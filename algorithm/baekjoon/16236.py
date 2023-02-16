# 빡구현 문제

n = int(input())
graph = []
for _ in range(n):
    graph.append(list(map(int, input().split())))

# 먹을 수 있는 물고기 체크
def find_fish():
    pass

# 가장 가까운 물고기 찾기
def dist():
    pass

ate = 0
size = 2
i=0

while(True):

    # 먹을 수 있는 물고기 없을 때
    if(find_fish()==0):
        break
    else:
        # 가장 가까운 물고기 먹음
        ate = ate + 1

        if(ate==size):
            size=size+1

        i=i+1

print(i)
