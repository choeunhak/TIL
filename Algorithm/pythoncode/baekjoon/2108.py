import sys
n = int(sys.stdin.readline())
nums=[]
for i in range(n):
    nums.append(int(sys.stdin.readline()))

def average(nums):
    return round(sum(nums)/len(nums))

def middle(nums):
    nums.sort()
    return nums[int(len(nums)/2)]

def frequency(nums):
    cnt_dict={}
    for i in nums:
        if(i in cnt_dict):
            cnt_dict[i]=cnt_dict[i]+1
        else:
            cnt_dict[i]=1
    sort_dict = [key for key, value in cnt_dict.items() if value == cnt_dict[max(cnt_dict, key=cnt_dict.get)]]
    # print(cnt_dict)
    # print(sort_dict)
    if(len(sort_dict)==1):
        return sort_dict[0]
    else:
        return (sort_dict[1])
    # return [i for i, value in enumerate(cnt) if value == max(cnt)][1]

def num_range(nums):
    return max(nums)-min(nums)

print(average(nums))
print(middle(nums))
print(frequency(nums))
print(num_range(nums))


# counter 써도 풀 수 있다는데 쓰지 않고 그냥 dict 이용함