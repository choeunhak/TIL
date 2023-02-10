def time2min(time):
    min = int(time[0:2])*60 + int(time[3:5])
    return min

def solution(m, musicinfos):
    answer_list = []

    # 시작한 시각, 끝난 시각, 음악 제목, 악보 정보

    # 시작~끝난 시각까지 음을 연장 또는 단축
    for i in range(len(musicinfos)):
        song = musicinfos[i].split(',')

        song_time = (time2min(song[1]) - time2min(song[0]))
        tmp = song_time//len(song[3])
        tmp_rest = song_time%len(song[3])
        tmp_sound = song[3] * tmp + song[3][0:tmp_rest]

        # 음 단축 처리해야함
        if(song_time < len(song[3])):
            tmp_sound = song[3][0:song_time]

        # m이 음 연장또는 단축한 거에 있나 확인
        # print(tmp_sound)
        for j in range(0, len(tmp_sound)-len(m)):
            # print(j)
            if(tmp_sound[j:j+len(m)] == m and tmp_sound[j+len(m)] != "#"):
                answer_list.append([song_time, song[1], song[2]])

    answer = ""
    if(not answer_list):
        answer = "(None)"
    else:
        tmp_sorted = sorted(answer_list, key = lambda x: (-x[0], x[1]))
        answer = tmp_sorted[0][2]
    return answer