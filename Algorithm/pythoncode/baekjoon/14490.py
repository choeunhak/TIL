ratio = input("")
ratio = ratio.split(':')
m = a = int(ratio[0])
n = b = int(ratio[1])

while(b!=0):
  a=a%b
  a,b=b,a
    
m = m//a
n = n//a

print(str(m)+":"+str(n))