# 파이썬 딕셔너리 사용법
dict={}

# value로 오름차순 정렬
sorted_dict = sorted(dict.items(), key=lambda x: x[1])

# value로 내림차순 정렬
sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)


# defaultdict
# 없는 키여도 keyerror를 일으키지 않는다.
from collections import defaultdict

# 아래와 같이 쓸경우 없는 키일때 list를 반환!
ex_dict = defaultdict(list)