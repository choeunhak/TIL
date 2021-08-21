participant=["leo", "kiki", "eden"]
completion=["eden", "kiki"]

def solution(participant, completion):
    d = dict()
    hashValue = 0
    for p in participant:
        d[hash(p)] = p
        hashValue += hash(p)
    for c in completion:
        hashValue -= hash(c)
    return d[hashValue]

print(solution(participant,completion))