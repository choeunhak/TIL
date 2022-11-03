n = int(input())
matrix=[]
for i in range(n):
  tmp = input()
  matrix.append(tmp)

friends = [[] for i in range(n)]

# print(friends)
for i in range(len(matrix)):
  for j in range(len(matrix[i])):
    if(matrix[i][j]=="Y"):
      friends[i].append(j)

# print(friends)

two_friends = friends.copy()

for i in range(len(friends)):
  for j in range(len(friends[i])):
    # print(j)
    # print(friends[i][j])
    two_friends[i]=two_friends[i]+friends[friends[i][j]]

# print(two_friends)

for i in range(len(two_friends)):
  two_friends[i]=set(two_friends[i])

for i in range(len(two_friends)):
  two_friends[i].discard(i)

# print(two_friends)
max_len=0
for i in range(len(two_friends)):
  if(len(two_friends[i])>max_len):
    max_len=len(two_friends[i])

print(max_len)
