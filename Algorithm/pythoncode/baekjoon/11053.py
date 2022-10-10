n=int(input())
nums=map(int, input().split())

last=0
cnt=0
for num in nums:
    if(num>last):
        cnt=cnt+1
        last=num

print(cnt)