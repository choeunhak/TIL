#9093
N = int(input())
for i in range(N):
    p=[]
    a=input().split()
    for t in a:
        for k in range(len(t)):
            p.append(t[k])
        while(True):
            print(p.pop(), end="")
            if(not p):
                break
        print(" ", end="")
        