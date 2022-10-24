def frequency(nums):
    cnt_dict={}
    for i in nums:
        i=i.upper()
        if(i in cnt_dict):
            cnt_dict[i]=cnt_dict[i]+1
        else:
            cnt_dict[i]=1

    sort_dict = [key for key, value in cnt_dict.items() if value == cnt_dict[max(cnt_dict, key=cnt_dict.get)]]

    if(len(sort_dict)==1):
        return sort_dict[0]
    else:
        return '?'

word = list(input())
print(frequency(word))