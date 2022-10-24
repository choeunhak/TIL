import math

def minTofullMin(minute):
    fullMin = int(minute[0:2])*60+int(minute[3:5])
    return fullMin

def solution(fees, records):
    answer = []
    car={}
    tmp={}
    for r in records:
        if(r[6:10] in tmp):
            if(r[6:10] in car):
                car[r[6:10]] = car[r[6:10]]+minTofullMin(r[0:5])-tmp[r[6:10]]
            else:
                car[r[6:10]] = minTofullMin(r[0:5])-tmp[r[6:10]]
            del tmp[r[6:10]]
        else:
            tmp[r[6:10]]=minTofullMin(r[0:5])
    for rest in tmp:
        if(rest in car):
            car[rest] = car[rest]+minTofullMin("23:59")-tmp[rest]
        else:
            car[rest] = minTofullMin("23:59")-tmp[rest]
    
    car = sorted(car.items())
    
    for c in car:
        if(c[1]<=fees[0]):
            answer.append(fees[1])
        else:
            tmp = fees[1]+math.ceil((c[1]-fees[0])/fees[2])*fees[3]
            answer.append(tmp)
    return answer

print(solution([180, 5000, 10, 600], ["07:59 0148 IN", "22:59 5961 IN", "23:00 5961 OUT"]))