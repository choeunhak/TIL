from itertools import combinations

n, s = map(int, input().split())
nums = list(map(int, input().split()))

cnt=0
for i in range(len(nums)):
  tmp_list = list(combinations(nums, i+1))
  for j in range(len(tmp_list)):
    if(sum(tmp_list[j])==s):
      cnt=cnt+1
# print(nums)
print(cnt)
