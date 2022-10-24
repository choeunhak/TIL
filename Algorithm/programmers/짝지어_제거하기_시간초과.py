# 재귀활용 풀이

def solution(s):
    s_array=list(s)
    # print(check(s_array))
    if(len(s_array)==0):
        return 1
    elif(s==check(s)):
        return 0
    else:
        return solution(check(s))

def check(s_array):
    i=0
    while(True):
        if(i+1>=len(s_array)):
            break
        if(s_array[i]==s_array[i+1]):
            s_array=s_array[0:i]+s_array[i+2:len(s_array)]
        i=i+1
    return s_array



print(solution("abcd"))