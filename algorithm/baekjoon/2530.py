#2530
a,b,c=map(int,input().split())
N=int(input())
s1=(c+N)%60
m1=(b+(c+N)//60)
m2=(m1%60)
h1=(a+m1//60)
h2=(h1%24)
print(h2, m2, s1)

# if(m>=60):
#     h=m//60
#     m=m%60
#     if((a+h)>=24):
#         print(a+h-24,b+m,c+s)
#     else:
#         print(a+h,b+m,c+s)
# else:
#     print(a,b+m,c+s)