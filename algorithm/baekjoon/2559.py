n, k = map(int, input().split())
data = list(map(int, input().split()))

tmp_val = sum(data[0:k])
max_val = tmp_val

# 처음에 k개만큼 더해줌
for i in range(k,n):
	tmp_val = tmp_val + data[i] # 다음 인덱스 더해줌
	tmp_val = tmp_val - data[i-k] # 이전 인덱스 빼줌
	max_val = max(tmp_val, max_val) # 더 큰값 구하기

print(max_val)
