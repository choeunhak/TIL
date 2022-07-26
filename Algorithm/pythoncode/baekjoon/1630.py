def eratosthenes2(N):
    nums = [1] * (N+1)
    for i in range(N+1):
        nums[i] = i

    nums[0] = 0
    nums[1] = 0

    sqrtn = int(N ** 0.5)

    for i in range(2, sqrtn+1):
        if nums[i] == i:
            # 가장 작은 소인수를 기록하여 최적화
            for j in range(i*i, N+1, i):
                if nums[j] == j:
                    nums[j] = i

    # nums 의 인자는 각 숫자의 소인수 분해를 위한 정보로 사용
    return nums

def factor(N):
    global nums

    ret = []

    while (N > 1):
        ret.append(nums[N])
        N //= nums[N]
    return ret


N = int(input())

# N 이하의 숫자들의 최소 소수
nums = eratosthenes2(N)

# N 이하의 숫자들의 최소 소수들을 이용하여 소인수분해 진행
for i in range(N+1):
    print(factor(i))