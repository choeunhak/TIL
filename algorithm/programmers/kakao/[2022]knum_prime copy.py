def isPrime(a):
    a=int(a)
    if(a<2):
        return False
    for i in range(2,a):
        if(a%i==0):
            return False
    return True
    
def solution(n, k):
    answer = 0
    tmp=""
    while(True):
        tmp=tmp+str(n%k)
        n=n//k
        if(n==0):
            break
    tmp_rev = ''
    for char in tmp:
        tmp_rev = char + tmp_rev
    
    tmp_num=""
    j=0
    while(j<len(tmp_rev)):
        k=j
        while(True):
            if(tmp_rev[k]=='0'):
                break
            elif(k==len(tmp_rev)-1):
                k=k+1
                break
            k=k+1
        tmp_num=tmp_rev[j:k]
        j=k
        if(tmp_num):
            if(isPrime(tmp_num)==True):
                answer=answer+1
        j=j+1
        
    return answer
# print(solution(437674, 3))
# print(solution(110011,10))
print(solution(1000000,3))
