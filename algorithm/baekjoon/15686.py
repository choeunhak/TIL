# 치킨 거리 = 집과 가장 가까운 치킨집 사이의 거리
# 도시의 치킨 거리는 모든 집의 치킨 거리의 합
from itertools import combinations
import copy


def dist(a, b, c, d):
  return abs(a - c) + abs(b - d)


n, m = map(int, input().split())
city = []
for i in range(n):
  city.append(list(map(int, input().split())))

chicken = []
all_chicken_dist = []

for i in range(n):
  for j in range(n):
    if (city[i][j] == 2):
      chicken.append([i, j])

chicken_case = list(combinations(chicken, m))

for case in range(len(chicken_case)):
  tmp_city = copy.deepcopy(city)
  #나머지 치킨집은 0으로 설정
  for i in range(n):
    for j in range(n):
      if (tmp_city[i][j] == 2 and [i, j] not in chicken_case[case]):
        tmp_city[i][j] = 0
  chicken_dist = []
  # 치킨 거리 계산
  for i in range(n):
    for j in range(n):
      tmp_chicken_dist = []
      if (tmp_city[i][j] == 1):
        for c in chicken_case[case]:
          tmp_chicken_dist.append(dist(i, j, c[0], c[1]))
        chicken_dist.append(min(tmp_chicken_dist))
  all_chicken_dist.append(sum(chicken_dist))

print(min(all_chicken_dist))
