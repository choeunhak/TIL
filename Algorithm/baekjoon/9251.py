a=input()
b=input()

# a="ACAYKP"
# b="CAPCAK"
ans=[]
for i in range(len(a)+1):
    ans.append([0]*(len(b)+1))
for i in range(1,len(a)+1):
    for j in range(1,len(b)+1):
        if(a[i-1]==b[j-1]):
            ans[i][j]=ans[i-1][j-1]+1
        else:
            ans[i][j]=max(ans[i-1][j],ans[i][j-1])

print(ans[len(a)][len(b)])