# deque는 list보다 속도가 빠르고, 쓰레드 환경에서 안전하기 때문이다.
# deque는 slicing이 불가하다
#pop(0)와 같은 메서드를 수행할 때 리스트의 경우 O(N)연산을 수행하지만 deque는 O(1) 연산을 수행한다.

from collections import deque



tmp = []
que = deque(tmp)
print(len(que))