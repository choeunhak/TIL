t=int(input())
def facto(n):
    i=n
    while(True):
        if(i==1):
            break
        i=i-1
        n=n*i
    return n

# print(facto(4))
for i in range(t):
    m,n = map(int, input().split())
    # print(facto(1))
    if(m==n):
        print(1)
    else:
        print(facto(n)//(facto(m)*facto(n-m)))

# 중복조합? -> 아님
# 조합인듯 n!x(n-m)! / m! 인듯?
# https://ko.numberempire.com/combinatorialcalculator.php
