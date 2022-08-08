n,m = map(int, input().split())
nums=[]
for i in range(n):
    nums.append(int(input()))

nums.sort()

i=0
result=int(2e9)
for end,val in enumerate(nums):
    # cur_sum=cur_sum+val
    if(nums[end]-nums[i]>=m):
        result=min(result,nums[end]-nums[i])
        # cur_sum=cur_sum-nums[i]
        i=i+1
print(result)



####################아래는 정답######################
# N, M = map(int, input().split())
# arr = [int(input()) for _ in range(N)]

# arr.sort()
# left, right = 0, 0
# result = int(2e9)

# while left < N and right < N:
#     if arr[right] - arr[left] < M:
#         right += 1
#     else:
#         result = min(result, arr[right] - arr[left])
#         left += 1

# print(result)
# 출처: https://sangminlog.tistory.com/entry/boj-2230 [로그 남기기:티스토리]