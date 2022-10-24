import math

def is_prime(x):
    if x == 0 or x == 1:
        return False
    for i in range(2, int(math.sqrt(x))+1):
        if x % i == 0:
            return False
    return True

n=int(input())
nums =list(map(int, input().split()))

cnt=0
for num in nums:
    if(is_prime(num)):
        cnt=cnt+1

print(cnt)