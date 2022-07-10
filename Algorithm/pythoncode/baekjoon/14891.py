# N극은 0, S극은 1

w1=list(input())
w2=list(input())
w3=list(input())
w4=list(input())

K=int(input())

def get_score(wheel):
    if(wheel[0]=='0'):
        return 0
    elif(wheel[0]=='1'):
        return 1

def turn_right(wheel):
    tmp=wheel.pop(7)
    wheel.insert(0,tmp)
    return wheel

def turn_left(wheel):
    tmp=wheel.pop(0)
    wheel.insert(7,tmp)
    return wheel

def isSameDir(a,b):
    if(a==b):
        return True
    elif(a!=b):
        return False

for i in range(K):
    num,dir = map(int,input().split())
    if(num==1):
        if(dir==-1):
            if(isSameDir(w1[2], w2[6])):
                w1=turn_left(w1)
            else:
                w1=turn_left(w1)
                w2=turn_right(w2)
        elif(dir==1):
            if(isSameDir(w1[2], w2[6])):
                w1=turn_right(w1)
            else:
                w1=turn_right(w1)
                w2=turn_left(w2)
    elif(num==2):
        if(dir==-1):
            if(isSameDir(w1[2], w2[6]) and isSameDir(w2[2], w3[6])):
                w2=turn_left(w2)
            elif(isSameDir(w1[2], w2[6]) and not isSameDir(w2[2], w3[6])):
                w2=turn_left(w2)
                w3=turn_right(w3)
            elif(not isSameDir(w1[2], w2[6]) and isSameDir(w2[2], w3[6])):
                w2=turn_left(w2)
                w1=turn_right(w1)
            else:
                w2=turn_left(w2)
                w1=turn_right(w1)
                w3=turn_right(w3)
        elif(dir==1):
            if(isSameDir(w1[2], w2[6]) and isSameDir(w2[2], w3[6])):
                w2=turn_right(w2)
            elif(isSameDir(w1[2], w2[6]) and not isSameDir(w2[2], w3[6])):
                w2=turn_right(w2)
                w3=turn_left(w3)
            elif(not isSameDir(w1[2], w2[6]) and isSameDir(w2[2], w3[6])):
                w2=turn_right(w2)
                w1=turn_left(w1)
            else:
                w2=turn_right(w2)
                w1=turn_left(w1)
                w3=turn_left(w3)
    elif(num==3):
        if(dir==-1):
            if(isSameDir(w2[2], w3[6]) and isSameDir(w3[2], w4[6])):
                w3=turn_left(w3)
            elif(isSameDir(w2[2], w3[6]) and not isSameDir(w3[2], w4[6])):
                w3=turn_left(w3)
                w4=turn_right(w4)
            elif(not isSameDir(w2[2], w3[6]) and isSameDir(w3[2], w4[6])):
                w3=turn_left(w3)
                w2=turn_right(w2)
            else:
                w3=turn_left(w3)
                w4=turn_right(w4)
                w2=turn_right(w2)
        elif(dir==1):
            if(isSameDir(w2[2], w3[6]) and isSameDir(w3[2], w4[6])):
                w3=turn_right(w3)
            elif(isSameDir(w2[2], w3[6]) and not isSameDir(w3[2], w4[6])):
                w3=turn_right(w3)
                w4=turn_left(w4)
            elif(not isSameDir(w2[2], w3[6]) and isSameDir(w3[2], w4[6])):
                w3=turn_right(w3)
                w2=turn_left(w2)
            else:
                w3=turn_right(w3)
                w4=turn_left(w4)
                w2=turn_left(w2)
    elif(num==4):
        if(dir==-1):
            if(isSameDir(w3[2], w4[6])):
                w4=turn_left(w4)
            else:
                w4=turn_left(w4)
                w3=turn_right(w3)
        elif(dir==1):
            if(isSameDir(w3[2], w4[6])):
                w4=turn_right(w4)
            else:
                w4=turn_right(w4)
                w3=turn_left(w3)
    print(w1)
    print(w2)
    print(w3)
    print(w4)
    print()
    
ans = get_score(w1) + 2*get_score(w2) + 4*get_score(w3) + 8*get_score(w4)

print(ans)