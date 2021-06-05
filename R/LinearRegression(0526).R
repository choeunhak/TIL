x=1:100

y=x^2+3*x+5+rnorm(100)
lm(y~I(x^2)+x)

y

x
