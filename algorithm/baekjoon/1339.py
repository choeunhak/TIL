# 이 생각을 어캐 하지...???
# 자릿수 큰 게 더 큰 숫자로 부여하는 것 까지는 알았는데
# 하나의 알파벳이 여러 번 나오는 경우 어떻게 처리할지 감이 안잡혔다.
# 예를 들면 GCG, ACDEB인 경우 G를 어떻게 처리할지...

# defaultdict으로 개선할 수 있다.

n = int(input())
words = []
word_dict = {}
for i in range(n):
    words.append(input())

# 알파벳의 자릿수 만큼 10에 곱해줘서 더해줌
for i in range(len(words)):
    for j in range(len(words[i])):
        if(words[i][j] in word_dict):
            word_dict[words[i][j]] = word_dict[words[i][j]] + 10**(len(words[i])-j)
        else:
            word_dict[words[i][j]] = 10**(len(words[i])-j)

# value로 정렬
sorted_word_dict = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)


# 차례대로 9부터 1까지 수 부여
result_dict = {}
n=9
for i in range(len(sorted_word_dict)):
    result_dict[sorted_word_dict[i][0]] = n
    n = n-1

# 결과값 계산, 다 더하기
answer = 0
for i in range(len(words)):
    for j in range(len(words[i])):
        answer = answer + result_dict[words[i][j]]*(10**(len(words[i])-j-1))

print(answer)

