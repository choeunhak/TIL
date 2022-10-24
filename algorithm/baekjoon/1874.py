import sys
n = int(sys.stdin.readline())

def isStackSequence(n):
    count = 1
    stack_range = []
    plus_minus = []
    nums = []
    for _ in range(n):
        nums.append(int(sys.stdin.readline()))
    for num in nums:
        while count <= num:
            stack_range.append(count)
            plus_minus.append('+')
            count += 1
        print(stack_range)
        print('num',num)
        if stack_range[-1] == num:
            stack_range.pop()
            plus_minus.append('-')
        else:
            return False
    return plus_minus

result = isStackSequence(n)
if result==False:
    print('NO')
else:
    for i in result :
        print(i)