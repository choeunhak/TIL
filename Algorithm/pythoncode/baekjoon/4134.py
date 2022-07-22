# https://www.acmicpc.net/problem/4134
import sys
import math
input = sys.stdin.readline

def isPrime(x):
    if x == 0 or x == 1:
        return False
    for i in range(2, int(math.sqrt(x))+1):
        if x % i == 0:
            return False
    return True

t = int(input())
for i in range(t):
    n = int(input())
    while True:
        if isPrime(n):
            print(n)
            break
        else:
            n += 1