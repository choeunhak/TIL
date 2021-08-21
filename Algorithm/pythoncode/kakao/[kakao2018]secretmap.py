#비밀지도

n=6
arr1=[46, 33, 33 ,22, 31, 50]
arr2=[27 ,56, 19, 14, 14, 10]

def solution(n, arr1, arr2):
    binarr1=[]
    binarr2=[]
    answer = []
    for i in range(n):
        if(n<1):
            break
        binarr1.append(bin(arr1[i])[2:])
        binarr2.append(bin(arr2[i])[2:])
        
    print(binarr1)
    print(binarr2)
    for i in range(n):
        t= n-len(binarr1[i])
        binarr1[i]=t*"0"+binarr1[i]
        t= n-len(binarr2[i])
        binarr2[i]=t*"0"+binarr2[i]

    for i in range(n):
        tempstr=""
        for j in range(len(binarr1[0])):
            if(binarr1[i][j]=='1' or binarr2[i][j]=='1'):
                tempstr=tempstr+"#"
            else:
                tempstr=tempstr+" "
        answer.append(tempstr)
    return answer

print(solution(n,arr1,arr2))
