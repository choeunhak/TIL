n,m = map(int, input().split())
nums=[]
for i in range(n):
    nums.append(int(input()))

nums.sort()


# 맞는 풀이
left=0
right=0
result=int(2e9)
while left < n and right < n:
    if(nums[right]-nums[left]>=m):
        result=min(result,nums[right]-nums[left])
        left=left+1
    else:
        right=right+1
print(result)

########################################################


# 틀린풀이
left=0
result=int(2e9)
for right in range(len(nums)):
    if(nums[right]-nums[left]>=m):
        result=min(result,nums[right]-nums[left])
        left=left+1
print(result)


########################################################

# 틀린 풀이
left=0
right=0
result=int(2e9)
while left < n and right < n:
    if(nums[right]-nums[left]>=m):
        result=min(result,nums[right]-nums[left])
        left=left+1
    right=right+1
print(result)