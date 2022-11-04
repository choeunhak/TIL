from itertools import combinations

n = int(input())
abilities = []
for i in range(n):
  abilities.append(list(map(int, input().split())))

diff = []


def get_diff(a, b):
  team1 = 0
  team2 = 0
  team1_case = list(combinations(a, 2))
  team2_case = list(combinations(b, 2))
  for i in range(len(team1_case)):
    team1 = team1 + abilities[team1_case[i][0]][team1_case[i][1]] + abilities[
      team1_case[i][1]][team1_case[i][0]]
  for i in range(len(team2_case)):
    team2 = team2 + abilities[team2_case[i][0]][team2_case[i][1]] + abilities[
      team2_case[i][1]][team2_case[i][0]]
  diff.append(abs(team1 - team2))


cases = list(combinations(range(n), len(abilities[0]) // 2))

for i in range(len(cases)):
  get_diff(cases[i], cases[len(cases) - i - 1])

print(min(diff))
