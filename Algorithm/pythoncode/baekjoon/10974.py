n=int(input())

num=[]
for i in range(n):
    num.append(i+1)


i=0
while(True):
    if(num[i]==n):
        break
    while(True):
        print(num[i], end=" ")
    
    i=i+1