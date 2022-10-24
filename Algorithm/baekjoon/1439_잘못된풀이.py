a=input()
cnt0=0
cnt1=0
i=0
j=0
while(True):
    if(i==len(a)-1):
        break
    # print(i)
    if(a[i]=='0'):
        cnt0=cnt0+1
        while(True):
            if(i==len(a)-1 or a[i]=='1'):
                break
            i=i+1
    if(a[i]=='1'):
        cnt1=cnt1+1
        while(True):
            if(i==len(a)-1 or a[i]=='0'):
                break
            i=i+1
    if(a[i]=='0'):
        cnt0=cnt0+1
        while(True):
            if(i==len(a)-1 or a[i]=='1'):
                break
            i=i+1


print(min(cnt0, cnt1))