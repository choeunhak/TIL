def solution(record):
    answer = []
    people={}
    for i in range(len(record)):
        tmp=record[i].split()
        if(tmp[0][0]=="E"):
            people[tmp[1]]=tmp[2]
        # elif(tmp[0][0]=="L"):
        #     if(tmp[1] in people):
        #         del people[tmp[1]]
        elif(tmp[0][0]=="C"):
            people[tmp[1]]=tmp[2]
    for i in range(len(record)):
        tmp=record[i].split()
        if(tmp[0][0]=="E"):
            answer.append(people[tmp[1]]+"님이 들어왔습니다.")
        elif(tmp[0][0]=="L"):
            # if(tmp[1] in people):
                answer.append(people[tmp[1]]+"님이 나갔습니다.")
    return answer

    

solution(["Leave uid3453", "Enter uid1234 Muzi", "Enter uid4567 Prodo","Leave uid1234","Enter uid1234 Prodo","Change uid4567 Ryan"])