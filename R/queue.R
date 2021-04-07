


queue = function(){
  q=c()
  q_size=0
  
  enqueue=function(data){
    q<<-c(q,data)
    q_size<<-q_size+1
  }
  
  dequeue=function(){
    first=q[1]
    q <<- q[-1]
    q_size<<- q_size -1
    return(first)
  }
  
  size=function(){
    return(q_size)
  }
  
  return(list(enqueue=enqueue, dequeue=dequeue, size=size))
}


q=queue()
q$enqueue(1)
q$enqueue(2)
q$size()