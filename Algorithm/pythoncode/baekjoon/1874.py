import sys
n = int(sys.stdin.readline())

def isStackSequence(n):
    count = 1
    stack_range = []
    plus_minus = []
    for i in range(n):
        num = int(sys.stdin.readline())
        while count <= num:
            stack_range.append(count)
            plus_minus.append('+')
            count += 1
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