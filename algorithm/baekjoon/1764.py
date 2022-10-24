n,m = map(int, input().split())

no_hear=[]
no_see=[]
for i in range(n):
    no_hear.append(input())

for i in range(m):
    no_see.append(input())

no_hear_see = set(no_hear) & set(no_see)

no_hear_see = list(no_hear_see)
no_hear_see.sort()
print(len(no_hear_see))

for i in no_hear_see:
    print(i)