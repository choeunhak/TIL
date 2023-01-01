# 2보다 큰 모든 짝수는 두 소수의 합으로 나타낼 수 있다는 것
import math

def is_prime(x):
    if x == 0 or x == 1:
        return False
    for i in range(2, int(math.sqrt(x))+1):
        if x % i == 0:
            return False
    return True

t = int(input())

for i in range(t):
    n = int(input())
    mid = n//2
    for i in range(mid, 0, -1):
        if(is_prime(i) and is_prime(n-i)):
            print(i, n-i)
            break
