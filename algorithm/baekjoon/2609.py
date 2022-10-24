#2609

a, b = input().split() 
a=int(a)
b=int(b)
if(a>=b):
    k=b
else:
    k=a
while(True):
    if(a%k==0 and b%k==0):
        break
    k=k-2

print(k)

if(a>=b):
    t=a
else:
    t=b
    
while(True):
    if(t%a==0 and t%b==0):
        break
    t=t+2

print(t)