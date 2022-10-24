#2420
a,b=map(int, input().split())
c=a-b
if(c<0):
    c=c-(c*2)
print(c)