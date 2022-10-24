def binary_search(target, data):
    data.sort()
    start = 0
    end = len(data) - 1

    while start <= end:
        mid = (start + end) // 2

        if data[mid] == target:
            return mid # 함수를 끝내버린다.
        elif data[mid] < target:
            start = mid + 1
        else:
            end = mid -1

    return mid


# 배열을 하나만 입력받는 경우 data.sort를 밖으로 빼서 시간복잡도를 줄일 수 있다.