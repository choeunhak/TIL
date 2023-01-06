import math
n, k = map(int, input().split())

# 1. 자연수의 분할
def partition(number, k):
    answer = set()
    answer.add((number, ))
    for x in range(1, number):
        for y in partition((number - x), k):
            if(len(tuple(sorted((x, ) + y)))<=k):
                answer.add(tuple(sorted((x, ) + y)))
    return answer

def check_count(case, k):
    total = math.factorial(k)
    tmp=1
    list_case = list(case)
    while(True):
        if(len(list_case)>=k):
            break
        list_case.append(0)
    list_case.append("c")
    # print(list_case)
    for i in range(len(list_case)-1):
        # print(total)
        if(list_case[i]==list_case[i+1]):
            tmp=tmp+1
        else:
            total = total // math.factorial(tmp)
            tmp=1
    return total

# 2. 각 경우의 수 계산
cases = partition(n, k)
answer = 0
for case in cases:
    # print(case)
    answer += check_count(case, k)
    # print("answer", answer)
print(answer)
