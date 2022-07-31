n=int(input())
points=[]
for i in range(n):
    x,y=map(int, input().split())
    points.append([x,y])


points = sorted(points, key=lambda a: a[1])
points = sorted(points, key=lambda a: a[0])

for i in range(len(points)):
    print(points[i][0],points[i][1])