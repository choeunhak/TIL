def d(n):
    n=str(n)
    tmp=0
    for i in range(len(n)):
        tmp=tmp+int(n[i])
    result=tmp+int(n)
    return result

tmp=[]
for i in range(10001):
    tmp.append(i)

d_num=[]
for i in range(10001):
    d_num.append(d(i))
self_num = set(tmp)-set(d_num)

self_num=list(self_num)

self_num.sort()
for i in self_num:
    print(i)