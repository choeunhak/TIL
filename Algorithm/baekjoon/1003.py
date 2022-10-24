t=int(input())


def fibo(n):
    fibo_list=[0,1,1,2]+[0]*n
    if(n==0):
        return [0,0,1]
    for i in range(3,n):
        fibo_list[i]=fibo_list[i-1]+fibo_list[i-2]
    return fibo_list
    # print(fibo_list)


for i in range(t):
    n=int(input())
    print(fibo(n)[n-1], fibo(n+1)[n])


