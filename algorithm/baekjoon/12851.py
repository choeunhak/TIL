from collections import deque

def bfs (node, k):
    # 큐 구현을 위한 deque 라이브러리 활용
    queue = deque([node])
    global cnt
    # 큐가 완전히 빌 때까지 반복
    while queue:
        # 큐에 삽입된 순서대로 노드 하나 꺼내기
        v = queue.popleft()
        if(v==k):
            cnt=cnt+1
        for i in (v-1, v+1, v*2):
            if(0<=i<max_val):
                if (dist[i]==-1) or (dist[i]==dist[v]+1):#방문한적 없거나 현재시간+1인경우, or 뒤에는 큐에 다시 집어넣기 위함이다
                    dist[i]=dist[v]+1
                    queue.append(i)
n, k = map(int, input().split())
max_val=10**5+1
cnt = 0
dist=[-1]*(max_val)
dist[n]=0
bfs(n, k)
print(dist[k])
print(cnt)