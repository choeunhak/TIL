n, m = map(int, input().split())
nums = list(map(int, input().split()))

nums.sort()

s = []
visited = []
def dfs():
    # print(s)
    if len(s)==m:
        result = ""
        for i in s:
            # if(nums[i-1] not in visited):
            result = result + str(nums[i-1])+" "

        if(result not in visited):
            print(result)
            visited.append(result)
        # print(' '.join(map(str,s)))
        return

    for i in range(1,n+1):
        if i not in s:
            s.append(i)
            dfs()
            s.pop()

dfs()