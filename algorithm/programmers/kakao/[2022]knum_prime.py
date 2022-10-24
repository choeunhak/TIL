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
    
    print(tmp_rev)
    tmp_num=""
    i=0
    t=0
    j=0
    while(j<len(tmp_rev)):
        if(tmp_rev[j]!='0'):
            i=j
            while(i<len(tmp_rev)):
                if(tmp_rev[i]=='0'):
                    break
                else:                         
                    tmp_num=tmp_num+tmp_rev[i]
                    i=i+1
                    j=j+1
            print(tmp_num)
            if(isPrime(tmp_num)==True):
                answer=answer+1
                tmp_num=""
        else:
            t=j
            while(t<len(tmp_rev)):
                if(tmp_rev[t]!='0'):
                    break
                else:
                    t=t+1
                    j=j+1
        # j=i+1
        
        

    # while(True):
    #     if(i=='0'):
    #         break
    #     tmp_num=tmp_num+i
    # print(tmp_num)
    # if(isPrime(tmp_num)==True):
    #     answer=answer+1
    # tmp_num=""
        
    return answer
print(solution(437674, 3))
# print(solution(110011,10))