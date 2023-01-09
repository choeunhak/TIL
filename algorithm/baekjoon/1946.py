import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    people = [list(map(int, input().split())) for _ in range(n)]
    people_sorted_by_doc = sorted(people)

    # [[1, 4], [2, 3], [3, 2], [4, 1], [5, 5]]
    # [[1, 4], [2, 5], [3, 6], [4, 2], [5, 7], [6, 1], [7, 3]]

    inter_of_first_doc = 0
    answer = 1

    for i in range(1, len(people_sorted_by_doc)):
        # 만약 인터뷰 점수가 서류 1등보다 높으면 채용을 시켜주고 그때의 인터뷰점수를 갱신시켜줘야한다, 그래서 정렬이 필요하다
        # people_sorted_by_doc[inter_of_first_doc][1]
        # 4, 3, 2, 1, 4
        # 4, 4, 4, 2, 2, 1, 3
        if people_sorted_by_doc[i][1] < people_sorted_by_doc[inter_of_first_doc][1]:
            inter_of_first_doc = i
            answer += 1

    print(answer)