# https://programming119.tistory.com/169


field = [
[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
[(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
[(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
[(3, 0), (3, 1), (3, 2), (3, 3), (3, 4)],
[(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
]
m,n = 2, 3

for i in range(len(field)-n):
    for j in range(len(field)-m):
        [row[j:j+m] for row in field[i:i+n]]