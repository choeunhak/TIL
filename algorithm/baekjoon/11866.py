n, k = map(int, input().split())

arr = []

for i in range(1, n+1):
    arr.append(i)

print("<", end="")
while(arr):
    # 12를 빼서 arr의 맨 뒤에 넣는다
    # arr의 맨 앞의 값을 뺀다
    # 다시 45를 빼서 맨 뒤에 넣는다
    # arr의 맨 앞의 값을 뺀다
    for i in range(k - 1):
        arr.append(arr[0])
        arr.pop(0)
    print(arr.pop(0), end="")
    if(arr):
        print(', ', end="")
print(">")
