n, k = map(int, input().split())

# deque 라이브러리 불러오기
from collections import deque

# BFS 메서드 정의
def bfs (node, k, visited):
    # 큐 구현을 위한 deque 라이브러리 활용
    queue = deque([node])
    # 현재 노드를 방문 처리
    visited.append(node)
    # 큐가 완전히 빌 때까지 반복
    while queue:
        # 큐에 삽입된 순서대로 노드 하나 꺼내기
        v = queue.popleft()
        if(v==k):
            print(dist[v])
            break
        # 탐색 순서 출력
        # 현재 처리 중인 노드에서 방문하지 않은 인접 노드를 모두 큐에 삽입
        for i in (v-1, v+1, 2*v):
            if 0<i<max_val and i not in visited:
                dist[i]=dist[v]+1
                queue.append(i)
                visited.append(i)

max_val=10**5
dist=[0]*(max_val+1)
graph=[]
visited = []
bfs(n, k, visited)