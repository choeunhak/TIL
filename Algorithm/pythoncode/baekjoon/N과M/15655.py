
n,m = map(int,input().split())
nums=list(map(int, input().split()))
nums.sort()

s = []
def dfs(start):
    if len(s)==m:
        for i in s:
            print(nums[i-1], end=" ")
        print()
        # print(' '.join(map(str,s)))
        return

    for i in range(start,n+1):
        if i not in s:
            s.append(i)
            dfs(i+1)
            s.pop()
dfs(1)
