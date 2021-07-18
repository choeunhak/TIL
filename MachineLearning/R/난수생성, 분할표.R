x=seq(0,16,length=100)
y=dnorm(x,mean=7.5, sd=1.5)
plot(x,y,type='l',
     xlab="Liters per day",
     ylab="Density",
     main="Water drunken by school children < 12 years old")

#4Î¶¨ÌÑ∞ ?ù¥?ïò?ùò Î¨? ÎßàÏã§ ?ôïÎ•?
pnorm(4, mean=7.5, sd=1.5, lower.tail = T)

#8Î¶¨ÌÑ∞ ?ù¥?ÉÅ?ùò Î¨? ÎßàÏã§ ?ôïÎ•?
pnorm(8, mean=7.5, sd=1.5, lower.tail = F)
lower = 8
upper = 15
i = x>=lower & x<upper
polygon(c(lower, x[i], upper), c(0, y[i],0),col="red")
abline(h=0,col="red")

pb = round(pnorm(8, mean=7.5, sd=1.5, lower.tail=F),2)
pb
pb.results=paste("Cumluative probability of a child drinking > 8L/day",
                 pb, sep=":")
title(pb.results)


#±‚√ ≈Î∞Ë∑Æ
mean(1:5)
var(1:5)
sd(1:5)
fivenum(1:11)
summary(1:11)
x=factor(c("a","b","c","c","c","d","d"))
x
table(x)
which.max(table(x))
names(table(x))[3]


#∫–«“«•
#frequency
table(c("a","b","a","d","e","d","a","c","a","b"))

CTable = data.frame(x=c("3","7","9","10"),
                    y=c("A1","B2","A1","B2"),
                    num = c(4,6,2,9))
CTable

xtabs(num~x, data=CTable)
xtabs(num~y, data=CTable)

temp = xtabs(num~x+y, data=CTable)

temp
addmargins(temp)

# contingency table: table(x,y)
str(Cars93)
Car_table_3 = with(Cars93, table(Type, Cylinders))
Car_table_3

# contingency table: xtabs(~x+y, data)
Car_table_4 = xtabs(~Type + Cylinders, data=Cars93)
Car_table_4
addmargins(Car_table_4)
