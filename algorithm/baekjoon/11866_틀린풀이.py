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
    arr.extend(arr[0:k-1])
    print("전", arr)
    for i in range(k - 1):
        arr.pop(0)
    # arr = arr[k-1:]
    print("후", arr)
    print(arr.pop(0), end="")
    if(arr):
        print(', ', end="")
print(">")
