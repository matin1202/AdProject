import time
import requests
import xml.etree.ElementTree as ET  # xml 정리를 위한 import
import xml.dom.minidom


from PyQt5.QtCore import QDate

import data_set

# API 리퀘스트를 위한 상수들
shortAPICode = """twI24Zuj+zOnrIovSaQLBosqt9GcqiA5IiLKurTshh3XwJ1xwSV8spaWWg6x8hHntYIRPGTUCCWcy+zHAeIR2g=="""
shortAPIUrl = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
middleAPICode = "twI24Zuj+zOnrIovSaQLBosqt9GcqiA5IiLKurTshh3XwJ1xwSV8spaWWg6x8hHntYIRPGTUCCWcy+zHAeIR2g=="
middleTempAPIUrl = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"
middleWeatherAPIUrl = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"


def requestShortWeather():  # 단기 예보 API 리퀘스트
    # API 가 받는 요소들
    params = {'serviceKey': shortAPICode, 'pageNo': '1', 'numOfRows': '1000', 'dataType': 'XML',
              'base_date': QDate.currentDate().toString('yyyyMMdd'), 'base_time': '0500', 'nx': '60', 'ny': '127'}

    # API 요청
    response = requests.get(shortAPIUrl, params=params)
    # str 형 API 응답을 xml 형식으로 전환
    parse = ET.fromstring(response.content.split(sep=b'</header>')[1].split(sep=b'</response>')[0])

    # 디버그를 위한 출력
    # dom = xml.dom.minidom.parseString(response.content)
    # print(dom.toprettyxml())

    # items 태그의 item 태그의 리스트를 리턴
    items = parse.findall('items/item')
    return items


def requestMiddleWeather():     # 중기 날씨, 기온 예보 API를 위한 리퀘스트
    # 기온 APi 가 받는 요소들
    temp_params = {'serviceKey': middleAPICode, 'pageNo': '1', 'numOfRows': '10', 'dataType': 'XML',
                   'regId': '11B10101', 'tmFc': QDate.currentDate().toString('yyyyMMdd') + '0600'}
    # 날씨 API 가 받는 요소들
    weather_params = {'serviceKey': middleAPICode, 'pageNo': '1', 'numOfRows': '10', 'dataType': 'XML',
                      'regId': '11B00000', 'tmFc': QDate.currentDate().toString('yyyyMMdd') + '0600'}

    # 기온 API 요청
    temp_response = requests.get(middleTempAPIUrl, params=temp_params)
    temp_parse = ET.fromstring(temp_response.content.split(sep=b'</header>')[1].split(sep=b'</response>')[0])

    # 디버그를 위한 출력
    # temp_dom = xml.dom.minidom.parseString(temp_response.content)
    # print(temp_dom.toprettyxml())

    temp_items = temp_parse.findall('items/item')

    # 공공 데이터 API 를 동시에 요청 할 수 없어 100ms의 간격을 둠
    time.sleep(0.1)

    # 날씨 API 요청
    weather_response = requests.get(middleWeatherAPIUrl, params=weather_params)
    weather_parse = ET.fromstring(weather_response.content.split(sep=b'</header>')[1].split(sep=b'</response>')[0])

    # 디버그를 위한 출력
    # weather_dom = xml.dom.minidom.parseString(weather_response.content)
    # print(weather_dom.toprettyxml())

    weather_items = weather_parse.findall('items/item')

    # 두 리스트를 통합해 리턴
    result = temp_items + weather_items
    return result


def requestWeatherStatus() -> list[data_set.dataSet]:   # 날씨 데이터를 요청
    # 단기 예보 데이터 리퀘스트
    shortWeather = requestShortWeather()
    # 중기 예보 데이터 리퀘스트
    middleWeather = requestMiddleWeather()

    # 일주일의 날씨 데이터를 저장하는 리스트
    dataSet: list[data_set.dataSet] = [data_set.dataSet(QDate.currentDate().addDays(x)) for x in range(8)]

    # 각각의 단기, 중기 예보 형식으로 되있는 xml 형식의 데이터를 dataSet 형식으로 변환
    data_set.shortXml2DataSet(shortWeather, dataSet)
    dataSet = data_set.middleXml2DataSet(middleWeather, dataSet)

    # 디버그를 위한 print
    for i in dataSet:
        print(str(i))

    return dataSet


# def getTemp(elements: list[xml.etree.ElementTree.Element]) -> list[int]:
#     result: list[int] = []
#     for i in elements:
#         if i.find('category').text == 'TMP':
#             result.append(int(i.find('fcstValue').text))
#     return result
