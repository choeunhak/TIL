def solution(places):
    ans = []
    for i in range(len(places)):
        flag=1
        for j in range(len(places[i])-2):
            for t in range(len(places[i][j])-2):
                if(places[i][j][t]=="P"):
                    if(places[i][j][t]==places[i][j][t+2]):
                        if(places[i][j][t+1]=="X"):
                            pass
                        else:
                            flag=0
                            break
                    elif(places[i][j][t]==places[i][j+2][t]):
                        if(places[i][j+1][t]=="X"):
                            pass
                        else:
                            flag=0
                            break
                    elif(places[i][j][t]==places[i][j+1][t+1]):
                        if(places[i][j+1][t]=="X" and places[i][j][t+1]=="X"):
                            pass
                        else:
                            flag=0
                            break
                    if(j>0):
                        if(places[i][j][t]==places[i][j-1][t+1]):
                            if(places[i][j][t+1]=="X" and places[i][j-1][t]=="X"):
                                pass
                            else:
                                flag=0
                                break
                    if(t>0):
                        if(places[i][j][t]==places[i][j+1][t-1]):
                            if(places[i][j+1][t]=="X" and places[i][j][t-1]=="X"):
                                pass
                            else:
                                flag=0
                                break
                    elif(places[i][j][t]==places[i][j+1][t]):
                        flag=0
                        break
                    elif(places[i][j][t]==places[i][j][t+1]):
                        flag=0
                        break
        for j in range(len(places[i])-1):
            for t in range(len(places[i][j])-1):
                if(places[i][j][t]=="P"):
                    if(places[i][j][t]==places[i][j+1][t+1]):
                        if(places[i][j+1][t]=="X" and places[i][j][t+1]=="X"):
                            pass
                        else:
                            flag=0
                            break
                    if(j>0):
                        if(places[i][j][t]==places[i][j-1][t+1]):
                            if(places[i][j][t+1]=="X" and places[i][j-1][t]=="X"):
                                pass
                            else:
                                flag=0
                                break
                    if(t>0):
                        if(places[i][j][t]==places[i][j+1][t-1]):
                            if(places[i][j+1][t]=="X" and places[i][j][t-1]=="X"):
                                pass
                            else:
                                flag=0
                                break
                    elif(places[i][j][t]==places[i][j+1][t]):
                        flag=0
                        break
                    elif(places[i][j][t]==places[i][j][t+1]):
                        flag=0
                        break
        ans.append(flag)

    return ans


places=[["POOOP", "OXXOX", "OPXPX", "OOXOX", "POXXP"], ["POOPX", "OXPXP", "PXXXO", "OXXXO", "OOOPP"], ["PXOPX", "OXOXP", "OXPOX", "OXXOP", "PXPOX"], ["OOOXX", "XOOOX", "OOOXX", "OXOOX", "OOOOO"], ["PXPXP", "XPXPX", "PXPXP", "XPXPX", "PXPXP"]]
print(solution(places))