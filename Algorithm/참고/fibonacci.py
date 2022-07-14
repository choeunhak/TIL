# 재귀
def fibonacci(i):
    if i==0:
        return 0
    elif i==1:
        return 1
    else:
        return fibonacci(i-1)+fibonacci(i-2)
for i in range(6):
    print(fibonacci(i))


#DP
fibo = [0 for i in range(100)]
fibo[0] = 0
fibo[1] = 1
for i in range(0,10):
    if i==0:
        print('0')
    elif i==1:
        print('1')
    else:
        fibo[i] = fibo[i-1] + fibo[i-2]
        print(fibo[i])