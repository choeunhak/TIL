n=int(input())

def makenum(n):
    if(n<10):
        n='0'+str(n)[0]
    n=str(n)
    tmp_sum=int(n[0])+int(n[1])
    new_num=str(n[-1])+str(tmp_sum)[-1]
    return new_num

cnt=0
result=n
while(True):
    result=makenum(int(result))
    # print(result)
    if(int(result)==n):
        break

    cnt=cnt+1
print(cnt+1)