n,m = list(map(int,input().split()))
 
s = []

def find_max(arr):
    if not arr:
        return 0
    else:
        return max(arr)

 
def dfs():
    if len(s)==m:
        print(' '.join(map(str,s)))
        return
    
    for i in range(1,n+1):
        if i not in s and find_max(s)<i :
            s.append(i)
            dfs()
            s.pop()
dfs()