n=int(input())

def is_group(word):
    tmp=[]
    for i in range(len(word)-1):
        if(word[i]!=word[i+1]):
            if(word[i+1] in tmp):
                return False
            else:
                tmp.append(word[i])

    # print(tmp)
    return True

cnt=0
for i in range(n):
    word=input()
    if(is_group(word)):
        cnt=cnt+1
print(cnt)