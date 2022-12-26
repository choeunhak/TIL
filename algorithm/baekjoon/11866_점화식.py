ret = []
n,k = map(int,input().split())
circle = [str(i+1) for i in range(n)]
dead = 0
while circle:
    dead = (dead + k -1) % len(circle)
    ret.append(circle.pop(dead))
print('<'+', '.join(ret)+'>')