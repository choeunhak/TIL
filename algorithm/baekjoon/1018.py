n, m = map(int, input().split())
chess=[]
for i in range(n):
    chess.append(input())

tmp=[]
w_start="WBWBWBWB"
b_start="BWBWBWBW"

def check_W(a,b,c,d,e,f,g,h):
    cnt=0
    for i in range(8):
        if(w_start[i]!=a[i]):
            cnt=cnt+1
    for i in range(8):
        if(b_start[i]!=b[i]):
            cnt=cnt+1
    for i in range(8):
        if(w_start[i]!=c[i]):
            cnt=cnt+1
    for i in range(8):
        if(b_start[i]!=d[i]):
            cnt=cnt+1
    for i in range(8):
        if(w_start[i]!=e[i]):
            cnt=cnt+1
    for i in range(8):
        if(b_start[i]!=f[i]):
            cnt=cnt+1
    for i in range(8):
        if(w_start[i]!=g[i]):
            cnt=cnt+1
    for i in range(8):
        if(b_start[i]!=h[i]):
            cnt=cnt+1
    return cnt

def check_B(a,b,c,d,e,f,g,h):
    cnt=0
    for i in range(8):
        if(b_start[i]!=a[i]):
            cnt=cnt+1
    for i in range(8):
        if(w_start[i]!=b[i]):
            cnt=cnt+1
    for i in range(8):
        if(b_start[i]!=c[i]):
            cnt=cnt+1
    for i in range(8):
        if(w_start[i]!=d[i]):
            cnt=cnt+1
    for i in range(8):
        if(b_start[i]!=e[i]):
            cnt=cnt+1
    for i in range(8):
        if(w_start[i]!=f[i]):
            cnt=cnt+1
    for i in range(8):
        if(b_start[i]!=g[i]):
            cnt=cnt+1
    for i in range(8):
        if(w_start[i]!=h[i]):
            cnt=cnt+1
    return cnt

def check(a,b,c,d,e,f,g,h):
    return min(check_W(a,b,c,d,e,f,g,h), check_B(a,b,c,d,e,f,g,h))

i=0
while(True):
    j=0
    while(True):
        if(j+7>m-1):
            break
        tmp.append(check(chess[i][j:j+8], chess[i+1][j:j+8], chess[i+2][j:j+8], chess[i+3][j:j+8], chess[i+4][j:j+8], chess[i+5][j:j+8], chess[i+6][j:j+8], chess[i+7][j:j+8]))
        j=j+1
    if(i+7==n-1):
        break
    i=i+1


print(min(tmp))