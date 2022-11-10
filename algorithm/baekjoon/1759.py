from itertools import combinations

l,c = map(int, input().split())
alphabets = map(str, input().split())

codes = list(combinations(alphabets, l))

list_codes = []
for code in codes:
  list_code = list(code)
  list_code.sort()
  vowel=0
  con=0
  for char in list_code:
    if(char in ['a', 'e', 'i', 'o', 'u']):
      vowel=vowel+1
    elif(65<=ord(char)<=90 or 97<=ord(char)<=122):
      con=con+1
  if(vowel>=1 and con>=2):
    list_codes.append(''.join(list_code))
list_codes.sort()
for code in list_codes:
  print(code)
# print(codes)
