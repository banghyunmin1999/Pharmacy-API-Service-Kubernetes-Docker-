from flask import Flask, Response
import os
import requests
import bs4
import pandas as pd
from dotenv import load_dotenv
import json

# .env 파일에서 환경변수 불러오기
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask 공공데이터 수집 서버 실행 중"

def collectPharmacyData():
    # API 키 로딩
    apiKey = os.getenv("API_KEY")
    if not apiKey:
        return {"error": "API_KEY 환경변수 없음"}, 500

    # URL 인코딩
    encoded_key = apiKey  


    # 수집할 지역
    targetNameList = ["강서구", "강남구", "강북구"]
    #데이터베이스 컬럼 명(수집할 태그 이름)[지역 ,  약국이름 , 위치)
    columnsList = ["지역", "dutyName", "dutyAddr"]

    # 수집 결과 저장 리스트
    dutyNameTagList = []
    dutyAddrTagList = []
    targetColumnsList = []

    for i in range(len(targetNameList)):
        hasPage = True
        k = 1
        while(hasPage):# 비어있는 페이지인지 체크 후 비어있으면 종료
            #목표 url
            targetUrl = f"http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire?serviceKey={encoded_key}&Q0=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&Q1={targetNameList[i]}&QT=1&ORD=NAME&pageNo={k}&numOfRows=10"

            # 요청 및 파싱
            reps = requests.get(targetUrl)
            htmlObj = reps.text
            print("응답 상태 코드:", reps.status_code)
            bsObj = bs4.BeautifulSoup(htmlObj, "lxml-xml")# xml 데이터 이므로 "lxml-xml" 로 parser
            ItemsTag = bsObj.find(name="items")

            # items 태그가 없을 경우
            if ItemsTag is None:
                print("items 태그 없음")
                return {"error": "ItemsTag is None"}, 500

            itemTag = ItemsTag.find_all(name="item")

            # 만약 itemTag 가 비어있다면 whlie문 종료
            if (not itemTag):
                print(f"{targetNameList[i]} 수집 완료")
                hasPage = False
                continue
            # 리스트에 수집한 데이터 담기
            for z in range (len (itemTag)):
                dutyNameTagList.append(itemTag[z].find(name = columnsList[1]).text)
                dutyAddrTagList.append(itemTag[z].find(name = columnsList[2]).text)
                targetColumnsList.append(targetNameList[i])

            # 페이지수 + 1
            k = k + 1
    # 수집한 데이터를 DataFrame으로 모으기
    df = pd.DataFrame(zip(targetColumnsList, dutyNameTagList, dutyAddrTagList), columns=columnsList)
    # df.append( pd.DataFrame(zip(targetColumnsList , dutyNameTagList, dutyAddrTagList ) , columns = columnsList))
    return df

@app.route("/startCollecting")
def start_collecting():
    resultDf = collectPharmacyData()

    if isinstance(resultDf, tuple):
        return Response(
            json.dumps(resultDf[0], ensure_ascii=False , indent=2), # indent=2 : 출력 깔끔하게 해줌
            status=resultDf[1],
            content_type='application/json; charset=utf-8'
        )

    return Response(
        json.dumps(resultDf.to_dict(orient="records"), ensure_ascii=False , indent=2),#  ensure_ascii=False : 한글 깨짐 방지
        content_type='application/json; charset=utf-8'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
