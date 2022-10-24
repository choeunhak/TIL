from ast import Str


n=int(input())
people=[]

for i in range(n):
    x,y = map(int, input().split())
    people.append([x,y])

result=[1]*n
for i in range(len(people)):
    for j in range(len(people)):
        if(people[i][0]<people[j][0] and people[i][1]<people[j][1]):
            result[i]=result[i]+1

print(' '.join(map(str,result)))