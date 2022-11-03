# 20퍼에서 계속 틀림

import itertools

l = int(input())
nums = list(map(int, input().split()))
n = int(input())

cand = []
start = 0
tmp_nums = []
nums.sort()
cnt = 0

if (n in nums):
  cnt = 0
else:
  for i in range(len(nums)):
    if (nums[i] > n):
      start = i - 1
      break
  for i in range(nums[start] + 1, nums[start + 1]):
    tmp_nums.append(i)

  cand = itertools.combinations(tmp_nums, 2)
  cand = list(cand)

  for i, j in cand:
    if (i <= n and n <= j):
      cnt = cnt + 1
print(cand)
print(cnt)
