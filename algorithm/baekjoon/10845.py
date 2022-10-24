#10845
import sys
#입력에 대해 배움 input()이 느릴때는 import sys하고 sys.stdin.readline()을 사용하자
#문자열 처리할 때 처음에 split하고 [0]으로 접근하는것도 괜찮은거같다

t = int(sys.stdin.readline())
l=[]
for i in range(t):
    m=sys.stdin.readline().split()
    if(m[0]=='size'):
        print(len(l))
    elif(m[0]=='empty'):
        if(len(l)==0):
            print(1)
        else:
            print(0)
    elif(m[0]=='front'):
        if(len(l)!=0):
            print(l[0])
        else:
            print(-1)
    elif(m[0]=='back'):
        if(len(l)!=0):
            print(l[len(l)-1])
        else:
            print(-1)
    elif(m[0]=='pop'):
        if(len(l)==0):
            print(-1)
        else:
            print(l[0])
            del l[0]
    else:
        l.append(int(m[1]))
        continue
          
        
        