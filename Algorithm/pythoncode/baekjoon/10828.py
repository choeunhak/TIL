import sys
n = int(sys.stdin.readline())
stack=[]
for i in range(n):
    inst=sys.stdin.readline()
    if(inst[0:2]=='pu'):
        a=inst.split()
        stack.append(a[1])
    elif(inst[0:2]=='po'):
        if(not stack):
            print(-1)
        else:
            print(stack[-1])
            del stack[-1]
    elif(inst[0:2]=='si'):
        print(len(stack))
    elif(inst[0:2]=='em'):
        if(not stack):
            print(1)
        else:
            print(0)
    elif(inst[0:2]=='to'):
        if(not stack):
            print(-1)
        else:
            print(stack[-1])
