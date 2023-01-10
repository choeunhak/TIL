import sys
input = sys.stdin.readline

n = int(input())
cards = list(map(int, input().split()))
m = int(input())
test = list(map(int, input().split()))
answer = []

cards.sort()

#이분탐색
def binary_search(target, data):
    start = 0
    end = len(data) - 1
    while start <= end:
        mid = (start + end) // 2
        if data[mid] == target:
            return True
        elif data[mid] < target:
            start = mid + 1
        else:
            end = mid -1
    return False
for i in range(len(test)):
    if(binary_search(test[i],cards)):
        print(1, end=" ")
    else:
        print(0, end=" ")