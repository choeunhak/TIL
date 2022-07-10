N, M = map(int, input().split())
a_list = list(map(int, input().split()))
b_list = list(map(int, input().split()))

result=[]

# for i in range(len(a_list)):
#     for j in range(len(b_list)):
#         if(i==len(a_list)-1):
#             result=result+b_list[j:-1]
#         elif(j==len(b_list)-1):
#             result=result+a_list[i:-1]
#         else:
#             if(a_list[i]>b_list[j]):
#                 result.append(b_list[j])
#             elif(a_list[i]<=b_list[j]):
#                 result.append(a_list[i])

a=0
b=0
while(a!=len(a_list) or b!=len(b_list)):
    if(a==len(a_list)):
        result.append(b_list[b])
        b=b+1
    elif(b==len(b_list)):
        result.append(a_list[a])
        a=a+1
    else:
        if(a_list[a]>b_list[b]):
            result.append(b_list[b])
            b=b+1
        elif(a_list[a]<=b_list[b]):
            result.append(a_list[a])
            a=a+1


print(*result)