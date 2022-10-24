import sys

input=sys.stdin.readline()

n=int(input)
nums=[]


for i in range(n):
    tmp=int(sys.stdin.readline())
    nums.append(tmp)

nums.sort()

for num in nums:
    print(num)