a=int(input())
moc = a//5
ans=[]
for i in range(moc+1):
    tmp=a-(i*5)
    if(tmp%3!=0):
        ans.append(-1)
    else:
        ans.append(i+(tmp//3))

minValue=-1
for i in ans:
    if(i!=-1):
        minValue=i
print(minValue)

# [0,0,1,0,1,2,0,2,3,2,3,4,3,0,3]
# [4]


#https://velog.io/@y7y1h13/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98%EB%B0%B1%EC%A4%80-2839%EB%B2%88-%EC%84%A4%ED%83%95-%EB%B0%B0%EB%8B%ACdppython

#아래 풀이도 통과함
# 3보다 5가 더 작은 값을 주기 때문인듯
# def solution(N):
#     sugar = [-1] * 5001
#     sugar[3] = sugar[5] = 1

#     for i in range(6, N + 1):
#         if i % 3 == 0:
#             sugar[i] = sugar[i - 3] + 1
#         if i % 5 == 0:
#             sugar[i] = sugar[i - 5] + 1
#         elif sugar[i - 3] > 0 and sugar[i - 5] > 0:
#             sugar[i] = min(sugar[i - 3], sugar[i - 5]) + 1
#     print(sugar[N])


# if __name__ == "__main__":
#     solution(N = int(input()))