from flask import Flask, request
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytimekr import pytimekr

application = Flask(__name__)


@application.route("/arrinfo/line6", methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    
    
    sname01 = ['안심역','각산역','반야월역','신기역','율하역','용계역','방촌역','해안역','동촌역','아양교역','동구청역','동대구역','신천역','칠성시장역','대구역','중앙로역','반월당역','명덕역','교대역','영대병원역',
    '현충로역','안지랑역','대명역','서부정류장역','송현역','월촌역','상인역','월배역','진천역','대곡역','화원역','설화명곡역']
    sname02 = ['영남대역','임당역','정평역','사월역','신매역','고산역','대공원역','연호역','담티역','만촌역','수성구청역','범어역','대구은행역','경대병원역','반월당역','청라언덕역','반고개역','내당역','두류역',
           '감삼역','죽전역','용산역','이곡역','성서산업단지역','계명대역','강창역','대실역','다사역','문양역']
    sname03 = ['용지역','범물역','지산역','수성못역','황금역','어린이회관역','수성구민운동장역','수성시장역','대봉교역','건들바위역','명덕역','남산역','신남역','서문시장역','달성공원역','북구청역','원대역',
           '팔달시장역','만평역','공단역','팔달역','매천시장역','매천역','태전역','구암역','칠곡운암역','동천역','팔거역','학정역','칠곡경대병원역']
    sinterval01 = [2,2,2,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,1,2,2,1,2,2,1,2,2,1,2,2,2]
    sinterval02 = [2,2,2,2,2,2,2,3,1,2,2,2,2,2,2,1,2,2,1,2,2,2,2,2,2,2,2,4]
    sinterval03 = [1,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,1,1,2,1,1,2,2,2,1,2,1,2,1]
    
    holiday = [pytimekr.newyear(),pytimekr.lunar_newyear(),pytimekr.samiljeol(),pytimekr.buddha(),pytimekr.children(),pytimekr.memorial(),pytimekr.independence(),
           pytimekr.chuseok(),pytimekr.foundation(),pytimekr.hangul(),pytimekr.christmas()]
    
    state = -1 # -1 : default, 0 : weekday, 1 : saturday, 2 : sunday and holiday
    timestamp = []
    upanddown = -1 # 1 : up(상행), 0 : down(하행)
    
    
    def CheckLineNumber(text1): # 호선 구분잣기
        if text1 in sname01:
            linenumber = 1
        elif text1 in sname02:
            linenumber = 2
        else :
            linenumber = 3
        return linenumber

    def WhatIsToday():
        now = datetime.now().weekday()
        if now not in holiday : #평일 : 0 토요일 : 1 휴일 : 2
            if now < 5:
                state = 0
            elif now == 5:
                state = 1
            else :
                state = 2
        else :
            state = 2
        return state

    def LoadData(text1,text2,text3): #출발역,휴일,csv
        temp1 = []
        temp2 = []
        state = text2
        if text1 == sname01[0] or text1 == sname02[0] or text1 == sname03[0]:
            if state == 0:
                temp1.append(text3['상행평일'].dropna().tolist())
            elif state == 1:
                temp1.append(text3['상행토요일'].dropna().tolist())
            else:
                temp1.append(text3['상행휴일'].dropna().tolist())
        elif text1 == sname01[-1] or text1 == sname02[-1] or text1 == sname03[-1]:
            if state == 0:
                temp2.append(text3['하행평일'].dropna().tolist())
            elif state == 1:
                temp2.append(text3['하행토요일'].dropna().tolist())
            else:
                temp2.append(text3['하행휴일'].dropna().tolist())
        else :
            if state == 0:
                temp1.append(text3['상행평일'].dropna().tolist())
                temp2.append(text3['하행평일'].dropna().tolist())
            elif state == 1:
                temp1.append(text3['상행토요일'].dropna().tolist())
                temp2.append(text3['하행토요일'].dropna().tolist())
            else :
                temp1.append(text3['상행휴일'].dropna().tolist())
                temp2.append(text3['하행휴일'].dropna().tolist())
        return temp1,temp2

    def WhenSubwayCome(linenum,text1):
        if linenum == 1:
            url = './subway1/' + str(sname01.index(text1)) + '.csv'
        elif linenum == 2:
            url = './subway2/' + str(sname02.index(text1)) + '.csv'
        else :
            url = './subway3/' + str(sname03.index(text1)) + '.csv'

        csv_test = pd.read_csv(url, encoding='cp949')
        stat = WhatIsToday()
        temp1,temp2 = LoadData(text1,stat,csv_test) #출발역,휴일,csv
        return temp1,temp2


    text = body['userRequest']['utterance']
    
    if '역' not in text :
        text = text+'역'
            
    linenum = CheckLineNumber(text)
    temp1,temp2 = WhenSubwayCome(linenum,text)
    now = datetime.now()
    timestamp1 = []
    timestamp2 = []
    index1 = -1
    index2 = -1

    if temp1:
        temp1 = temp1[0]

        for item in temp1:
            timestamp1.append(item.split(':'))

        for idx, value in enumerate(timestamp1):
            if int(datetime.time(now).hour) >= int(value[0]) and int(datetime.time(now).minute) > int(value[1]):
                index1 = idx
        timestamp1 = timestamp1[index1 + 1:]
        print(timestamp1)

    if temp2:
        temp2 = temp2[0]

        for item in temp2:
            timestamp2.append(item.split(':'))
        for idx, value in enumerate(timestamp2):
            if int(datetime.time(now).hour) >= int(value[0]) and int(datetime.time(now).minute) > int(value[1]):
                index2 = idx
        timestamp2 = timestamp2[index2 + 1:]
        print(timestamp2)

    if linenum == 1:
        desti1 = "설화명곡"
        desti2 = "안심"
    elif linenum == 2:
        desti1 = "문양"
        desti2 = "영남대"
    else :
        desti1 = "칠곡경대병원"
        desti2 = "용지"

    if not timestamp1 and timestamp2:
        print(datetime.now())
        print(desti2 + "방면 도착 예정 시간은 " + timestamp2[0][0] + " 시 "+timestamp2[0][1] +" 분 입니다.")
        output = desti2 + "방면 도착 예정 시간은 " + timestamp2[0][0] + " 시 "+timestamp2[0][1] +" 분 입니다."
    elif timestamp1 and not timestamp2:
        print(datetime.now())
        print(desti1 + "방면 도착 예정 시간은 " + timestamp1[0][0] + " 시 " + timestamp1[0][1] + " 분 입니다.")
        output = desti1 + "방면 도착 예정 시간은 " + timestamp1[0][0] + " 시 " + timestamp1[0][1] + " 분 입니다."
    else :
        print(datetime.now())
        print(desti1 + "방면 도착 예정 시간은 " + timestamp1[0][0] + " 시 " + timestamp1[0][1] + " 분 입니다.")
        print(desti2 + "방면 도착 예정 시간은 " + timestamp2[0][0] + " 시 " + timestamp2[0][1] + " 분 입니다.")
        output = desti1 + "방면 도착 예정 시간은 " + timestamp1[0][0] + " 시 " + timestamp1[0][1] + " 분 입니다.\n" + desti2 + "방면 도착 예정 시간은 " + timestamp2[0][0] + " 시 " + timestamp2[0][1] + " 분 입니다."
        
        
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output
                    }
                }
            ]
        }
    }

    return responseBody

@application.route("/arrinfo/line3", methods=['POST'])
def line3_arrtm():
    now = datetime.now()
    time = str(now.hour).zfill(2)+str(now.minute).zfill(2)+str(now.second).zfill(2)
    
    weekno = datetime.today().weekday()    
    weekday = 0   
    if weekno < 5:
        weekday = 8 # 평일   
    elif weekno == 6 :
        weekday = 7 # 토요일
    elif weekno == 7:
        weekday = 9 # 휴일

    f = pd.read_csv('station_info.csv', encoding = 'cp949')
    find_row = f.loc[(f['RAIL_OPR_ISTT_NM'] == '대구도시철도')]
    new_find_row = find_row.values.tolist()

    stcd = find_row['STIN_CD'].tolist()
    stnm = find_row['STIN_NM'].tolist()
    dictionary = dict(zip(stnm,stcd))
    

    body = request.get_json()
    #print(body)
    stationname = body['userRequest']['utterance']
    stationname = stationname[1:]
    print(stationname)
    findname = dictionary[stationname]
    
    linecode = 0
    for line in new_find_row :
        #print(line)
        if line[5] == stationname :
            linecode = line[2]
            
    url = "http://openapi.kric.go.kr/openapi/trainUseInfo/subwayTimetable?serviceKey=$2a$10$jdJGVD.bxBIfm1cbCh.UVOd6Bg.LAks9WIpYQjrBoGiMzqQNmZeXu&format=xml&railOprIsttCd=DG&dayCd=%s&lnCd=%s&stinCd=%s" % (weekday,linecode,findname)
    print(url)
    result = requests.get(url)
    bsoup = BeautifulSoup(result.text, "html.parser")

    items = 0
    if stationname == '칠곡경대병원' or stationname == '용지' :
        items1 = bsoup.find_all("dpttm")
        items2 = bsoup.find_all("arvtm")
        items = items1 + items2
    else :
        items = bsoup.find_all("arvtm")

    stationarrtm = list()
    new_stationarrtm = []
    check = 0
    for idx, i in enumerate(items) :
        i = str(i.text)
        if i.startswith('05') or i.startswith('06') :
            check = idx
            break
    for j in items[check:]:
        j = str(j.text)
        new_stationarrtm.append(j)
        
    maxtm = time
    near = 0
    max_hr = str(time[:2])
    max_mn = str(time[2:4])
    max_sc = str(time[4:])
    
    response_text1 = 0
    response_text2 = 0
    for near in new_stationarrtm :
        if maxtm < near :
            #print(maxtm, near)
            near_hr = str(near[:2])
            near_mn = str(near[2:4])
            near_sc = str(near[4:])
        
            response_text1 = '현재 시간은 '+max_hr+'시 '+max_mn+'분 '+max_sc+'초이며,\n열차의 도착 시간은 '+near_hr+'시 '+near_mn+'분 '+near_sc+'초로\n'
            #print("현재 시간은 ",end='')
            #print(max_hr+"시 "+max_mn+"분 "+max_sc+"초이며,")
            #print("열차의")
            #print("도착 시간은 ",end='')
            #print(near_hr+"시 "+near_mn+"분 "+near_sc+"초로")
        
            max_time = max_hr+':'+max_mn+':'+max_sc
            near_time = near_hr+':'+near_mn+':'+near_sc
            time_1 = datetime.strptime(max_time,"%H:%M:%S")
            time_2 = datetime.strptime(near_time,"%H:%M:%S")
            time_interval = time_2 - time_1
 
            if (int(near) - int(maxtm)) >= 100 :
                minutes = (time_interval.seconds // 60)
                seconds = (time_interval.seconds % 60)
                #print(str(minutes) +" 분 " + str(seconds) +" 초 남았습니다.")
                response_text2 = str(minutes) +"분 " + str(seconds) +" 초 남았습니다."
            elif (int(near) - int(maxtm)) < 100 :
                seconds = (time_interval.seconds % 60)
                #print(str(minutes) +" 분 " + str(seconds) +" 초 남았습니다.")
                response_text2 = str(seconds) +" 초 남았습니다."
            else :
                print("운행중인 차량이 없습니다")
            break
            
    responseBody = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": response_text1 + response_text2
                }
            }
        ]
    }
}
    return responseBody



@application.route("/arrinfo/line99", methods=['POST'])
def innervoice():
    responseBody = {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": "여러분, 집에 갑시다."
                }
            }
        ]
    }
}
    return responseBody





@application.route("/")
def hello():
    return "Hello goorm!"


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)