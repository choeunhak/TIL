n, m = map(int, input().split())
nums = list(map(int, input().split()))

nums.sort()

s = []
visited = []
def dfs(start):
    if len(s)==m:
        result = ""
        for i in s:
            result = result + str(nums[i-1])+" "

        if(result not in visited):
            print(result)
            visited.append(result)
        return

    for i in range(start,n+1):
        # if i not in s:
            s.append(i)
            dfs(i)
            s.pop()

dfs(1)