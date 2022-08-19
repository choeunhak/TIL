

n=int(input())
cnt_dict={}
for i in range(n):
    book = input()
    if(book in cnt_dict):
        cnt_dict[book]=cnt_dict[book]+1
    else:
        cnt_dict[book]=1

# 딕셔너리에서 최댓값 찾기 max(cnt_dict, key=cnt_dict.get)
# 딕셔너리에서 최댓값이 들어있는 key들을 list로 반환해줌
max_val_dict = [key for key, value in cnt_dict.items() if value == cnt_dict[max(cnt_dict, key=cnt_dict.get)]]

max_val_dict.sort()
print(max_val_dict[0])