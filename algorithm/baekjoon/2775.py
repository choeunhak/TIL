t = int(input())
apartment = [[0 for _ in range(15)] for _ in range(15)]

for i in range(len(apartment)):
    apartment[0][i] =i+1
# print(apartment)
for i in range(1, len(apartment)):
    for j in range(len(apartment)):
        # print(i,j)
        apartment[i][j-1] = sum(apartment[i-1][0:j])
# print(apartment)

for i in range(t):
    k = int(input())
    n = int(input())
    print(apartment[k][n-1])