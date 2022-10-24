#sum(bridge)에서 시간이 좀 오래걸리는데 이거를 해결하려고 sum(bridge)를 따로 변수로 놓고 처리하였다.
#큐 다리를 지나는 트
def solution(bridge_length, weight, truck_weights):
    bridge = [0]*bridge_length
    answer = 0
    total=sum(bridge)
    
    while(True):
        if(len(truck_weights)==0 and total==0):
            break
        
        answer += 1
        if(bridge[0]!=0):
            total=total-bridge[0]#다리에서 나갈때 빼준다
        del bridge[0]
        
        if(len(truck_weights)!=0):
            if(total+truck_weights[0]<=weight):
                bridge.append(truck_weights[0])
                total=total+truck_weights[0]#전체무게에 더해준다
                del truck_weights[0]
            else:
                bridge.append(0)
        print(bridge)
            
    return answer
solution(2, 10, [7,4,5,6])
