import sys

t = int(sys.stdin.readline())
for i in range(t):
    n = int(sys.stdin.readline())
    answer = 0
    inter_of_first_doc = 0
    doc_of_first_inter = 0
    people = []
    for i in range(n):
        doc, inter = map(int, sys.stdin.readline().split())
        if(doc == 1):
            inter_of_first_doc = inter
        if(inter == 1):
            doc_of_first_inter = doc
        people.append([doc, inter])
    for i in range(len(people)):
        if(people[i][0] <= doc_of_first_inter and people[i][1] <= inter_of_first_doc):
            answer = answer+1
    print(answer)


# 이풀이는 틀린 풀이다
# 반례는
# 1, 4, 1 4, 4 1, 2 2, 3 3을 입력해보면 알 수 있다.
# 3 3 은 2 2때문에 탈락인데 합격으로 판정하기 때문이다.