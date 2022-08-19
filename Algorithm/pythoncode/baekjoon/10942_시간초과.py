n=int(input())
nums=list(map(int,input().split()))
ques=int(input())


# 스택 활용
def ispalin(words):
    # print(words)
    if(not words):
        return 1
    tmp=[]
    if(len(words)%2==0):#짝수
        for i in range(int(len(words)/2)):
            tmp.append(words[i])
        for i in range(int(len(words)/2),len(words)):
            if(tmp.pop()!=words[i]):
                return 0
    elif(len(words)%2==1):#홀수
        for i in range(int(len(words)/2)):
            tmp.append(words[i])
        for i in range(int(len(words)/2)+1,len(words)):
            if(tmp.pop()!=words[i]):
                return 0
    return 1


for _ in range(ques):
    start, end = map(int,input().split())
    print(ispalin(nums[start-1:end]))