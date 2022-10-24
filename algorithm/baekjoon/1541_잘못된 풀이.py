# print(55-(50+40))

# print(55-(50+40+40))

# 55-50+40+40-30
# -가 나오면 -가 나오지 전까지 괄호를 친다

import re

new_sik=""
sik = input()
# sik_split=re.split(r'[-+]', sik)
i=0
last=0
flag=False
# print(len(sik))
while(True):
    if(i>=len(sik)):
        break
    print(i)
    if(sik[i]=='-'):
        flag=True
        start=i
        new_sik=new_sik+sik[last:start+1]+'('
        i=i+1
        while(True):
            if(i+1==len(sik)):
                break
            if(sik[i+1]=='-'):
                break
            i=i+1
        last=i+1
        new_sik=new_sik+sik[start+1:i+1]+')'
    i=i+1
if(flag==False):
    new_sik=sik
# print(new_sik)
print(eval(new_sik))


#eval 사용 불가 따라서 틀림