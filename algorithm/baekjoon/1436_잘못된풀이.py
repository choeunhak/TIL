n=int(input())

list666=[]

for j in range(100):
    tmp=int('666'+str(j))
    if(tmp not in list666):
        list666.append(tmp)
    tmp2=int(str(j)+'666')
    if(tmp2 not in list666):
        list666.append(tmp2)
    for i in range(1000):
        tmp3=int(str(j)+'666'+str(i))
        if(tmp3 not in list666):
            print(tmp3)
            list666.append(tmp3)

list666.sort()

print(list666)
print(list666[n-1])