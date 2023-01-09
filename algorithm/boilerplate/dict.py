# 파이썬 딕셔너리 사용법
dict={}

# value로 오름차순 정렬
sorted_dict = sorted(dict.items(), key=lambda x: x[1])

# value로 내림차순 정렬
sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)