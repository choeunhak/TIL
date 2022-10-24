tmp=input()

cnt=0
i=0
while(True):
    if(i==len(tmp)):
        break
    if(tmp[i:i+3]=='dz='):
        cnt=cnt+1
        i=i+3
    elif(tmp[i:i+2]=='lj' or tmp[i:i+2]=='nj'):
        cnt=cnt+1
        i=i+2
    elif(tmp[i:i+2]=='c=' or tmp[i:i+2]=='c-' or tmp[i:i+2]=='d-' or tmp[i:i+2]=='s=' or tmp[i:i+2]=='z='):
        cnt=cnt+1
        i=i+2
    else:
        cnt=cnt+1
        i=i+1
print(cnt)
