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