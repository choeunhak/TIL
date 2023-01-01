def find_longest(candy):
    n=len(candy)
    answer=1
    for i in range(n):
        cnt=1
        for j in range(1, n):
            if candy[i][j] == candy[i][j-1]:
                cnt = cnt + 1
            else:
                cnt = 1
            if cnt > answer:
                answer = cnt
        cnt=1
        for j in range(1, n):
            if candy[j][i] == candy[j-1][i]:
                cnt = cnt + 1
            else:
                cnt = 1
            if cnt > answer:
                answer = cnt
    return answer

n = int(input())
candy = [list(input()) for _ in range(n)]
answer=0

for i in range(n):
    for j in range(n):
        if j+1 < n:
            candy[i][j], candy[i][j+1] = candy[i][j+1], candy[i][j]
            tmp=find_longest(candy)
            if tmp > answer:
                answer = tmp
            candy[i][j], candy[i][j+1] = candy[i][j+1], candy[i][j]
        if i+1 < n:
            candy[i][j], candy[i+1][j] = candy[i+1][j], candy[i][j]
            tmp=find_longest(candy)
            if tmp > answer:
                answer = tmp
            candy[i][j], candy[i+1][j] = candy[i+1][j], candy[i][j]

print(answer)