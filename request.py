import time
import data_set
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom


from PyQt5.QtCore import QDate

import data_set

shortAPICode = 'twI24Zuj+zOnrIovSaQLBosqt9GcqiA5IiLKurTshh3XwJ1xwSV8spaWWg6x8hHntYIRPGTUCCWcy+zHAeIR2g=='
shortAPIUrl = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
middleAPICode = "twI24Zuj+zOnrIovSaQLBosqt9GcqiA5IiLKurTshh3XwJ1xwSV8spaWWg6x8hHntYIRPGTUCCWcy+zHAeIR2g=="
middleTempAPIUrl = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"
middleWeatherAPIUrl = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"


def requestShortWeather():
    params = {'serviceKey': shortAPICode, 'pageNo': '1', 'numOfRows': '1000', 'dataType': 'XML',
              'base_date': QDate.currentDate().toString('yyyyMMdd'), 'base_time': '0500', 'nx': '60', 'ny': '127'}

    response = requests.get(shortAPIUrl, params=params)
    parse = ET.fromstring(response.content.split(sep=b'</header>')[1].split(sep=b'</response>')[0])
    dom = xml.dom.minidom.parseString(response.content)
    items = parse.findall('items/item')
    result = []
    return items


def requestMiddleWeather():
    temp_params = {'serviceKey': middleAPICode, 'pageNo': '1', 'numOfRows': '10', 'dataType': 'XML',
                   'regId': '11B10101', 'tmFc': QDate.currentDate().toString('yyyyMMdd') + '0600'}
    weather_params = {'serviceKey': middleAPICode, 'pageNo': '1', 'numOfRows': '10', 'dataType': 'XML',
                      'regId': '11B00000', 'tmFc': QDate.currentDate().toString('yyyyMMdd') + '0600'}

    temp_response = requests.get(middleTempAPIUrl, params=temp_params)
    temp_parse = ET.fromstring(temp_response.content.split(sep=b'</header>')[1].split(sep=b'</response>')[0])
    temp_dom = xml.dom.minidom.parseString(temp_response.content)
    temp_items = temp_parse.findall('items/item')

    time.sleep(0.1)

    weather_response = requests.get(middleWeatherAPIUrl, params=weather_params)
    weather_parse = ET.fromstring(weather_response.content.split(sep=b'</header>')[1].split(sep=b'</response>')[0])
    weather_dom = xml.dom.minidom.parseString(weather_response.content)
    weather_items = weather_parse.findall('items/item')

    result = temp_items + weather_items
    return result


def requestWeatherStatus() -> list[data_set.dataSet]:
    shortWeather = requestShortWeather()
    middleWeather = requestMiddleWeather()
    dataSet: list[data_set.dataSet] = [data_set.dataSet(QDate.currentDate().addDays(x)) for x in range(8)]
    data_set.shortXml2DataSet(shortWeather, dataSet)
    dataSet = data_set.middleXml2DataSet(middleWeather, dataSet)
    for i in dataSet:
        print(str(i))
    return dataSet


def getTemp(elements: list[xml.etree.ElementTree.Element]) -> list[int]:
    result: list[int] = []
    for i in elements:
        if i.find('category').text == 'TMP':
            result.append(int(i.find('fcstValue').text))
    return result
