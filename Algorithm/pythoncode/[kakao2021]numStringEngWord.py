eng=["zero","one","two","three","four","five","six","seven","eight","nine"]
num=[0,1,2,3,4,5,6,7,8,9]

def solution(s):
    answer = 0
    for i in range(len(eng)):
        if(eng[i] in s):
            s=s.replace(eng[i],str(num[i]))
    answer=int(s)
    return answer
