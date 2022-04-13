from flask import Flask, request
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup


# 현재모집중인과정_리스트
@app.route('/api/listCard', methods=['POST'])
def listCard():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    url = "http://www.kb.or.kr/p/?j=23"
    htmlText = requests.get(url).text
    bsoup = BeautifulSoup(htmlText, "html.parser")
    btab = bsoup.find("table", {"class":"tbl-c tbl-fix"})
    btbody = btab.find('tbody').find_all('td')
    links = btab.find_all('a')

    count = 0
    lst = []
    link_lst = []

    for a in links:
        count += 1
        if count % 2 == 1:
            href = a.attrs['href']
            link_lst.append("http://kb.or.kr/"+href)

    for i in range(len(btbody)):
        if i % 2 == 1:
            lst.append(btbody[i].text.split('\n'))

    cpart = []
    cname = []
    cperiod = []

    for i in range(len(lst)):
        cpart.append(lst[i][1])
        cname.append(lst[i][2])
        if '교육기간' in lst[i][3]:
            cperiod.append(lst[i][3])
        else:
            cperiod.append(lst[i][4])

    responseBody = {
            "version": "2.0",
        "template":{
            "outputs": [
                {
                    "listCard": {
                            "header": {
                        "title":"현재 모집중인 과정소개"
                        },
                       "items": [
                           {
                               "title": cname[0],
                               "description": cperiod[0],
                               "link": {
                                   "web": link_lst[0]
                               }
                           },
                           {
                               "title": cname[1],
                               "description": cperiod[1],
                               "link":{
                                   "web": link_lst[1]
                               }
                           },
                           {
                               "title": cname[2],
                               "description": cperiod[2],
                               "link": {
                                   "web": link_lst[2]
                               }
                           },
                           {
                               "title": cname[3],
                               "description": cperiod[3],
                               "link": {
                                   "web": link_lst[3]
                               }
                           },
                           {
                               "title": cname[4],
                               "description": cperiod[4],
                               "link": {
                                   "web": link_lst[4]
                               }
                           }
                       ],
                        "buttons":
                        [
                            {
                                "label": "수강신청하기",
                                "action": "webLink",
                                "webLinkUrl": "http://www.kb.or.kr/p/?j=27"
                            }
                        ]
                    }
                }
            ]
        }
    }
    return responseBody


# 현재모집중인과정_이미지
@app.route('/api/imagelist', methods=['POST'])
def imagelist():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    url = "http://kb.or.kr"
    htmlText = requests.get(url).text
    bsoup = BeautifulSoup(htmlText, "html.parser")
    bdiv = bsoup.find("div", {"id":"j-contents"})
    img = bdiv.find_all('img')[1:]

    # 이미지 src
    imgurl = []
    hrefurl = []
    cnt = 0
    href = 0
    for i in img :
        if cnt == 8 :
            break
        imgurl.append(url+i.get("src"))
        ref = i.get("onclick")
        href = ref[ref.find('/'):-1]
        hrefurl.append(url+href)
        cnt = cnt + 1

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[0]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[0]
                                    }
                                ]
                            },
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[1]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[1]
                                    }
                                ]
                            },
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[2]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[2]
                                    }
                                ]
                            },
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[3]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[3]
                                    }
                                ]
                            },
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[4]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[4]
                                    }
                                ]
                            },
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[5]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[5]
                                    }
                                ]
                            },
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[6]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[6]
                                    }
                                ]
                            },
                            {
                                "thumbnail": {
                                    "imageUrl": imgurl[7]
                                },
                                "buttons": [
                                    {
                                        "action":  "webLink",
                                        "label": "과정상세보기",
                                        "webLinkUrl": hrefurl[7]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
    return responseBody


# Test 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": '''안녕하세요. 만나서 반가워요.'''
                    }
                }
            ]
        }
    }

    return responseBody


# Test 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)