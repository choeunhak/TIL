name = str(input())
if(len(name)==1):
    print(name)
else:
    name_list=list(name)
    answer=""
    last=""
    # 아이디어 1
    # 1. 정렬
    name_list.sort()

    # 2. 알파벳별로 개수 세서 짝수면 절반개수 까지 빼내고 홀수면 -1 하고 절반 까지만 빼냄

    tmp=1
    ans=""
    last=""
    palin_flag=0
    for i in range(1, len(name_list)):

        if(name_list[i]==name_list[i-1]):
            tmp=tmp+1
        elif(name_list[i]!=name_list[i-1]):
            #홀수
            if(tmp%2==1):
                palin_flag=palin_flag+1
                last=name_list[i-1]
                ans=ans+name_list[i-1]*(tmp//2)
            #짝수
            else:
                ans=ans+name_list[i-1]*(tmp//2)
            tmp=1
        # 마지막 문자일 때
        if(i==len(name_list)-1):
            # 홀수
            if(tmp%2==1):
                palin_flag=palin_flag+1
                last=name_list[i]
                ans=ans+name_list[i-1]*(tmp//2)
            # 짝수
            else:
                ans=ans+name_list[i-1]*(tmp//2)     
        if(palin_flag>=2):
            break     


    ans=ans+last+ans[::-1]

    if(palin_flag>=2):
        print("I'm Sorry Hansoo")
    else:
        print(ans)
