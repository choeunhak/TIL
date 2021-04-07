
#스택 구현


stack=function(){
  s=c()
  s_size=0
  
  push = function(data) {
    if(full()==FALSE){
      s<<-c(s,data)
      s_size <<-s_size+1
    }else{
      print("스택이 꽉 찼습니다.")
    }
    
  }
  
  pop = function(){
    if(empty()==FALSE){
      last=s[length(s)]
      s<<-s[-length(s)]
      s_size <<-s_size-1
      return(last)
    }
    else{
      print("스택이 비었습니다.")
    }
    
  }
  
  size=function(){
    return(s_size)
  }
  
  empty=function(){
    if(s_size==0){
      return(TRUE)
    }
    else{
      return(FALSE)
    }
  }
  
  full=function(){
    if(s_size==20){
      return(TRUE)
    }
    else{
      return(FALSE)
    }
  }
  
# print=function(){
#    i=0
#    while(i<length(s)){
#      i=i+1
#      cat(s[i],"\n")
#    }
#  }
  return(list(push=push, pop=pop, size=size, empty=empty, full=full))
}

s=stack()
s$empty()
s$push(3)
s$push(4)
s$push(3)
s$push(4)
s$push(7)

s$push(3)
s$push(4)
s$push(7)
s$push(3)
s$push(4)

s$push(4)
s$push(7)
s$push(3)
s$push(4)
s$push(7)

s$push(4)
s$push(7)
s$push(3)
s$push(4)
s$push(7)
s$empty()
s$size()
s$full()
s$pop()
