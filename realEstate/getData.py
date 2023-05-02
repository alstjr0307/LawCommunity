from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import requests
import json
import pandas as pd
from datetime import datetime,timedelta
import warnings
import xmltodict # 결과가 xml 형식으로 반환된다. 이것을 dict 로 바꿔주는 라이브러리다
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import urllib.request as req
#국토교통부_아파트 매매 자료encoding = '본인의 API키(인코딩)'
decoding = 'r79Zg483c55po5YS7L25I+mblqD66ethH8+/mtOy8ckl3wrNiBoIj8L7jI9UpXZEbiAh70vJY092hp0UM67L+A=='

# 법정동 코드
areacode = 41173 

# 조회기간 설정 변수
month_digit = ['01','02','03','04','05','06','07','08','09','10','11','12'] 
search_year = '2023'

# 총 거래내역
count = []
df = pd.DataFrame()
rowList=[]  # 전체 행을 저장할 변수
nameList=[] # 열(칼럼) 이름을 저장할 변수
item_content=[] # 각 행별 칼럼값들을 저장할 임시공간

# 추출 모듈
for each in month_digit:
    yearmonth = search_year + each

    # url 입력
    url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev'
    params ={'serviceKey' : decoding, 'pageNo' : '1', 'numOfRows' : '10000', 'LAWD_CD' : areacode, 'DEAL_YMD' : yearmonth }

    response = requests.get(url, params=params).text
    xmlobj = BeautifulSoup(response, 'lxml-xml')
    rows = xmlobj.findAll('item')
    j = 0
    count.append(len(rows)) # 해당 기간의 거래내역 개수 저장
    rowsLen = len(rows)


    # 거래별 세부 항목 정리
    for i in range(rowsLen):
        columns = rows[i].find_all() # 1번째 행(row)의 모든 요소값들을 칼럼으로 한다.
        columnsLen = len(columns)    # 1번째 행(row)의 요소길이를 열(column) 길이로 한다.

        for j in range(0, columnsLen):
            if i == 0 and columns[j].name not in nameList:    # 첫번째 행 데이터 수집시 컬럼 값 저장
                nameList.append(columns[j].name)    # name 값만 추출한다

            eachColumn = columns[j].text    # 각 행(i)의 각 열(j)의 텍스트만 추출한다.
            item_content.append(eachColumn)   # 각 칼럼값을 append하여 1개 행을 만든다.
        rowList.append(item_content)    # 전체 리스트 공간에 개별 행을 append한다.
        item_content=[] # 다음 row의 값을 입력받기 위해 비워준다.

print(f'총 {sum(count)}개의 거래내역이 확인되었습니다.')
print(nameList, rowList)
df = pd.DataFrame(rowList, columns = nameList)
df.to_csv('data.csv', index=False)