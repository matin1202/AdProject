import xml.etree.ElementTree
import sys

from PyQt5.QtCore import QDate


class dataSet:

    def __init__(self, date: QDate) -> None:
        self.date: QDate = date
        self.minTemp: int = sys.maxsize
        self.maxTemp: int = -sys.maxsize
        self.am_weather: str = "Unknown"
        self.pm_weather: str = "Unknown"
        self.rainProb: int = -1

    def __str__(self):
        return self.date.toString('yyyy년 MM월 dd일') + ", 최저 온도 : " + str(self.minTemp)\
               + ", 최고 온도 : " + str(self.maxTemp) + ", 오전 날씨 : " + self.am_weather\
               + ", 오후 날씨 : " + self.pm_weather + ", 강수 확률 : " + str(self.rainProb) + "%"

    def __eq__(self, other):
        return self.date.toString('yyyyMMdd') == other


def shortXml2DataSet(element_list: list[xml.etree.ElementTree.Element], dataset: list[dataSet]):
    # response Code ("코드", "설명", "리턴 타입")
    # response_code = [
    #     ("POP", "강수 확률", "%"),     ("PTY", "강수 형태", "Code"),  ("PCP", "시간당 강수량", "mm"),
    #     ("REH", "습도", "%"),         ("SNO", "시간당 적설량", "mm"), ("SKY", "하늘 상태", "Code"),
    #     ("TMP", "기온", "C"),         ("TMN", "최저 기온", "C"),     ("TMX", "최고 기온", "C"),
    #     ("UUU", "풍속(동서)", "m/s"),  ("VVV", "풍속(남북)", "m/s"),  ("WAV", "파고", "m"),
    #     ("VEC", "풍향", "도"),         ("WSD", "풍속", "m/s"),       ("", "", ""),
    # ]
    # sky_status_code = [
    #     ("맑음", 1), ("구름많음", 3), ("흐림", 4)
    # ]
    # rain_type_code = [
    #     ("비", 1), ("진눈깨비", 2), ("눈", 3), ("소나기", 4)
    # ]

    sky_status = ["", "맑음", "", "구름많음", "흐림"]
    rain_type = ["", "비", "진눈깨비", "눈", "소나기"]

    weather = [
        [
            [0, -3, 0, 0, 0],
            [0, -3, 0, 0, 0]
        ] for _ in range(4)
    ]
    rain = [
        [
            False,
            False
        ] for _ in range(4)
    ]

    for item in element_list:
        isPm = True
        idx = -1
        category = item.find('category').text
        fcstValue = item.find('fcstValue').text

        for i in range(len(dataset)):
            if dataset[i] == item.find('fcstDate').text:
                idx = i

        if int(item.find('fcstTime').text) < 1200:
            isPm = False

        if category == "TMP":
            if dataset[idx].maxTemp < int(fcstValue):
                dataset[idx].maxTemp = int(fcstValue)
            if dataset[idx].minTemp > int(fcstValue):
                dataset[idx].minTemp = int(fcstValue)

        elif category == "POP":
            if dataset[idx].rainProb < int(fcstValue):
                dataset[idx].rainProb = int(fcstValue)

        elif category == "SKY":
            time = 1 if isPm else 0
            weather[idx][time][int(fcstValue)] += 1
            am_weather = 0
            pm_weather = 0
            for i in range(5):
                if am_weather < weather[idx][0][i]:
                    am_weather = weather[idx][0][i]
                    dataset[idx].am_weather = sky_status[i]
                if pm_weather < weather[idx][1][i]:
                    pm_weather = weather[idx][1][i]
                    dataset[idx].pm_weather = sky_status[i]

        elif category == "PTY":
            if int(fcstValue) != 0 and not rain[idx][1 if isPm else 0]:
                if isPm:
                    if dataset[idx].pm_weather == "흐림":
                        dataset[idx].pm_weather = "흐리고 " + rain_type[int(fcstValue)]
                else:
                    dataset[idx].am_weather = "흐리고 " + rain_type[int(fcstValue)]

    return dataset


def middleXml2DataSet(element_list: list[xml.etree.ElementTree.Element], dataset: list[dataSet]):
    tElement = element_list[0]
    wElement = element_list[1]
    for i in range(len(tElement)):
        tag = tElement[i].tag
        txt = tElement[i].text
        if tag.find('ta') == -1 or tag.find('Low') != -1 or tag.find('High') != -1:
            continue
        if int(tag[5]) < 3 or int(tag[5]) > 7:
            continue
        if tag[:5] == "taMin":
            dataset[int(tag[5])].minTemp = int(txt)
        elif tag[:5] == "taMax":
            dataset[int(tag[5])].maxTemp = int(txt)
    for i in range(len(wElement)):
        tag = wElement[i].tag
        txt = wElement[i].text
        if tag == 'regId' or not (tag.find('Am') != -1 or tag.find('Pm') != -1):
            continue
        if tag[:4] == 'rnSt':  # Tag is Prediction of Rain Probability
            if dataset[int(tag[4])].rainProb < int(txt):
                dataset[int(tag[4])].rainProb = int(txt)
        elif tag[:2] == 'wf':  # Tag is Prediction of Weather
            if tag.find('Am') != -1:
                dataset[int(tag[2])].am_weather = txt
            else:
                dataset[int(tag[2])].pm_weather = txt

    return dataset
