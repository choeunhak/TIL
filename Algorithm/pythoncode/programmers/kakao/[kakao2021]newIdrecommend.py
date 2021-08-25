#다음에 다시 풀기
new_id="...!@BaT#*..y.abcdefghijklm"
new_id="=.="
special="~!@#$%^&*()=+[{]}:?,<>/"

def solution(new_id):
       answer = ''
       answer=new_id.lower()
       for i in range(len(special)):
              if(special[i] in answer):
                     answer=answer.replace(special[i],"")
       # print(answer)
       #3
       
       i=0
       while(i<len(answer)):
              if(len(answer)==1):
                     break
              t=i
              if(answer[i]=='.'):
                     while(True):
                            if(answer[i]!='.' or i==len(answer)-1):
                                   break
                            i=i+1
                     answer=answer[0:t]+'.'+answer[i:len(answer)]
              i=i+1
              
       # print(answer)
       if(answer[0]=='.'):
              answer=answer[1:len(answer)]
       if(len(answer)>1 and answer[len(answer)-1]=='.'):
              answer=answer[0:len(answer)-1]

       #5
       if(answer==""):
              answer="a"
       #6
       if(len(answer)>=16):
              answer=answer[0:15]
       if(answer[len(answer)-1]=='.'):
              answer=answer[0:len(answer)-1]
       #7
       if(len(answer)<=2):
              while(True):
                     if(len(answer)==3):
                            break
                     answer=answer+answer[len(answer)-1]
       return answer

print(solution(new_id))