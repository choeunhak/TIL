fibo=function(n){
  if(n==1||n==2){
    return(1)
  }
  return(fibo(n-1)+fibo(n-2))
}

fibo(3)

fibo(5)