N,L = map(int,input().split())

tape = list(map(int,input().split()))

tape.sort()

loc = 0
cnt = 0

for i in tape:
    print('loc',loc)
    print('i',i)
    if loc < i:
        loc = i+L-1
        cnt += 1

print(cnt)