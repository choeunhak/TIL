i=int(input())

def correct(st):
    if(len(st)%2==1):
        print("NO")
        return
    s=list(st)
    k=len(st)
    i=0
    t=[]
    while(k>0):
        if(s[i]=='('):
            t.append(s[i])
        if(s[i]==')' and not t):
            print("NO")
            return
        elif(s[i]==')'):
            t.pop()
        k=k-1
        i=i+1
    if(not t):
        print("YES")
        return
    else:
        print("NO")
        return
        
while(i>0):
    st=input()
    correct(st)
    i=i-1