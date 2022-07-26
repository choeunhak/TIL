# N개의 자연수 중에서 M개를 고른 수열

n,m = map(int, input().split())
nums=list(map(int, input().split()))
nums.sort()

s = []

def dfs():
    if len(s)==m:
        for i in s:
            print(nums[i-1], end=" ")
        print()
        # print(' '.join(map(str,s)))
        return

    for i in range(1,n+1):
        if i not in s:
            s.append(i)
            dfs()
            s.pop()
dfs()