# 반례
# 4 4
# 0 0 0 0
# 0 0 0 0
# 0 0 1 2
# 0 0 3 4


n, m = map(int, input().split())
arr = []

for _ in range(n):
    arr.append(list(map(int, input().split())))


def get_tmp_max(tmp):
    tmp_result = []

    for k in range(len(tmp)):
        for i in range(0, len(arr)-len(tmp[k])+1):
            for j in range(0, len(arr[0])-len(tmp[k][0])+1):

                # 원래 배열 슬라이스
                tmp_arr = [row[j:j+len(tmp[k][0])] for row in arr[i:i+len(tmp[k])]]

                # 슬라이스랑 tmp 배열 비교해서 1이면 다 더하기
                tmp_sum = 0
                for m in range(len(tmp_arr)):
                    for n in range(len(tmp_arr[0])):
                        if(tmp[k][m][n]==1):
                            tmp_sum = tmp_sum + tmp_arr[m][n]

                tmp_result.append(tmp_sum)
    return max(tmp_result)

# 회전....
def type1():
    tmp1 = [[1,1,1,1]]
    tmp2 = [[1], [1], [1], [1]]

    tmp = [tmp1] + [tmp2]

    return get_tmp_max(tmp)

def type2():
    tmp1 = [[1,1]*2]

    tmp = [tmp1]

    return get_tmp_max(tmp)

def type3():
    tmp1 = [[1,0],[1,0],[1,1]]
    tmp2 = [[0,1],[0,1],[1,1]]
    tmp3 = [[1,1],[1,0],[1,0]]
    tmp4 = [[1,1],[0,1],[0,1]]
    tmp5 = [[1,1,1],[0,0,1]]
    tmp6 = [[1,1,1],[1,0,0]]
    tmp7 = [[0,0,1],[1,1,1]]
    tmp8 = [[1,0,0],[1,1,1]]

    tmp = [tmp1] + [tmp2] + [tmp3] + [tmp4] + [tmp5] + [tmp6] + [tmp7] + [tmp8]

    return get_tmp_max(tmp)

def type4():
    tmp1 = [[1,0], [1,1], [0,1]]
    tmp2 = [[0,1], [1,1], [1,0]]
    tmp3 = [[1,1,0], [0,1,1]]
    tmp4 = [[0,1,1], [1,1,0]]

    tmp = [tmp1] + [tmp2] + [tmp3] + [tmp4]

    return get_tmp_max(tmp)

def type5():
    tmp1 = [[1,1,1], [0,1,0]]
    tmp2 = [[0,1,0], [1,1,1]]
    tmp3 = [[1,0], [1,1], [1,0]]
    tmp4 = [[0,1], [1,1], [0,1]]

    tmp = [tmp1] + [tmp2] + [tmp3] + [tmp4]

    return get_tmp_max(tmp)


result = []
result.append(type1())
result.append(type2())
result.append(type3())
result.append(type4())
result.append(type5())

print(max(result))
