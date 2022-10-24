m=int(input())
n=int(input())

def isPrime(n):
    if(n==1):
        return False
    for i in range(2, n):
        if(n%i==0):
            return False
    return True

result=[]
while(True):
    if(m==n+1):
        break
    if(isPrime(m)):
        result.append(m)
    m=m+1

# print(result)
if(not result):
    print(-1)
else:
    print(sum(result))
    print(result[0])