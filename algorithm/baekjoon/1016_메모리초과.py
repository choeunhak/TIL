mi, ma = map(int, input().split())

# 정수 x가 1보다 큰 제곱수로 나누어 떨어지지 않을때...


n=ma
a = [False,False] + [True]*(n-1)
prime_square=[]

for i in range(2,n+1):
  if a[i]:
    prime_square.append(i**2)
    for j in range(2*i, n+1, i):
        a[j] = False

answer = 0
for i in range(mi, ma+1):
    flag=False
    for j in prime_square:
        # print(i,j)
        if(i%j==0):
            flag=True
            break
    if(flag==False):
        answer = answer+1


print(answer)