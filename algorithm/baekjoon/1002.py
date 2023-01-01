t = int(input())

def dist(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

#https://itstory1592.tistory.com/33 참조
for i in range(t):
    x1, y1, r1, x2, y2, r2 = map(int, input().split())

    circle_dist = dist(x1,y1,x2,y2)
    if(circle_dist==0):
        if(r1==r2):
            print(-1)
        else:
            print(0)
    else:
        if(r1+r2==circle_dist or abs(r1-r2)==circle_dist):
            print(1)
        elif((abs(r1-r2))<circle_dist) and (circle_dist<r1+r2):
            print(2)
        else:
            print(0)