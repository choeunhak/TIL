T = 10
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    n = int(input())
    apartments = list(map(int, input().split()))
    answer = 0
    # 왼쪽 1,2개 오른쪽 1,2개를 뺀 숫자를 더함!
    for i in range(2,len(apartments)-2):
        tmp_max_apartment = max(apartments[i-2], apartments[i-1], apartments[i+1], apartments[i+2])
        if((apartments[i]-tmp_max_apartment) > 0):
            answer = answer + apartments[i] -tmp_max_apartment
    print("#{}".format(test_case), answer)
