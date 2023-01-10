# data는 정렬되어있어야함

def binary_search(target, data):
    start = 0
    end = len(data) - 1

    while start <= end:
        mid = (start + end) // 2
        # 찾은 경우인듯
        if data[mid] == target:
            return mid # 함수를 끝내버린다.
        elif data[mid] < target:
            start = mid + 1
        else:
            end = mid -1

    # 찾지 못한 경우인듯(배열에 없는 타겟)
    return mid