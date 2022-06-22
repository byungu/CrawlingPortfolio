import json
import urllib.request
import datetime

import pandas as pd

ServiceKey = "4f55626c7763686138356a42676368"


def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success"%(datetime.datetime.now()))
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def getComentData(start):
    url = 'http://openapi.seoul.go.kr:8088/' + ServiceKey+'/json/ChunmanFreeSuggestions/%d/%d' % (start, start+4)
    retData = getRequestUrl(url)
    if (retData == None):
        return None
    else:
        return json.loads(retData)


def getSeoulSearch(nVoteScore):
    jsonResult = []
    result = []
    for i in range(1000//5):
        jsonData = getComentData(i*5 +1)
        if (jsonData['ChunmanFreeSuggestions']['RESULT']['CODE'] == 'INFO-100'):
            print('인증키가 유효하지 않습니다.!!')
            return

        if (jsonData['ChunmanFreeSuggestions']['RESULT']['CODE'] == 'INFO-000'):
            for i in range(5):
                if (jsonData['ChunmanFreeSuggestions']['row'][i]['VOTE_SCORE'] >= nVoteScore):
                    SN = jsonData['ChunmanFreeSuggestions']['row'][i]['SN']
                    TITLE = jsonData['ChunmanFreeSuggestions']['row'][i]['TITLE']
                    CONTENT_link = jsonData['ChunmanFreeSuggestions']['row'][i]['CONTENT']
                    DATE = jsonData['ChunmanFreeSuggestions']['row'][i]['REG_DATE']
                    VOTE = jsonData['ChunmanFreeSuggestions']['row'][i]['VOTE_SCORE']
                    jsonResult.append({'number': SN,
                                       'title': TITLE,
                                       'content': CONTENT_link,
                                       'date': DATE,
                                       'vote_score': VOTE})
                    result.append([SN, TITLE, CONTENT_link, DATE, VOTE])
    return (jsonResult, result)


def main():

    print("<< '민주주의 서울 자유제안' 득표수에 따른 데이터 1000개를 수집합니다. >>")
    nVoteScore = int(input('득표수를 지정 하세요 : '))

    jsonResult = []
    result = []
    jsonResult, result = getSeoulSearch(nVoteScore)

    with open('./서울_자유제안_득표수_%d이상.json'%(nVoteScore), 'w', encoding='utf8') as outflie:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys= True, ensure_ascii=False)
        outflie.write(jsonFile)

    columns = ['SN', 'TITLE', 'CONTENT_link', 'DATE', 'VOTE']
    result_df = pd.DataFrame(result, columns=columns)
    result_df.to_csv('./서울_자유제안_득표수_%d이상.csv' % (nVoteScore), index=False, encoding='cp949')

if __name__ == '__main__':
    main()