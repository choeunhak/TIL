

def solution(s):
    deg=1
    count=[]
    while(deg<=len(s)/2):
        i=0
        res=""
        while(i<=len(s)-1):
            t=1
            while(True):
                # print(s[i:i+deg])
                # print(s[i+deg:i+deg+deg])
                if(s[i:i+deg]!=s[i+deg:i+deg+deg]):
                    break
                i=i+deg
                t=t+1
            if(t==1):
                res=res+s[i:i+deg]
            else:
                res=res+str(t)+s[i:i+deg]
            i=i+deg
        # print(res)
        count.append(len(res))
        deg=deg+1
    # print(count)
    if(len(count)>1):
        answer = min(count)
    else:
        answer=1
    return answer
print(solution("a"))