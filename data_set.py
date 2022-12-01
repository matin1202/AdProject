import xml.etree.ElementTree
import sys

from PyQt5.QtCore import QDate


class dataSet:  # 날씨 데이터를 저장할 dataSet 형식

    def __init__(self, date: QDate, minTemp: int = sys.maxsize, maxTemp: int = -sys.maxsize, am_weather: str = "Unknown"
                 , pm_weather: str = "Unknown", rainProb: int = -1) -> None:
        # self.date: 날짜를 저장
        # self.minTemp: 해당 일의 최저 기온을 저장
        # self.maxTemp: 해당 일의 최고 기온을 저장
        # self.am_weather: 해당 일의 오전 날씨를 저장
        # self.pm_weather: 해당 일의 오후 날씨를 저장
        # self.rainProb: 해당 일의 강수 확률을 % 단위로 저장
        self.date: QDate = date
        self.minTemp: int = minTemp
        self.maxTemp: int = maxTemp
        self.am_weather: str = am_weather
        self.pm_weather: str = pm_weather
        self.rainProb: int = rainProb

    def __str__(self):  # 출력 방식 오버라이드
        return self.date.toString('yyyy년 MM월 dd일') + ", 최저 온도 : " + str(self.minTemp)\
               + ", 최고 온도 : " + str(self.maxTemp) + ", 오전 날씨 : " + self.am_weather\
               + ", 오후 날씨 : " + self.pm_weather + ", 강수 확률 : " + str(self.rainProb) + "%"

    def __eq__(self, other):  # 등호 연산 날짜로 구분하게 오버라이드
        return self.date.toString('yyyyMMdd') == other


def shortXml2DataSet(element_list: list[xml.etree.ElementTree.Element], dataset: list[dataSet]):
    # 단기 예보를 dataSet 형식으로 전환
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

    # 상수들
    sky_status = ["", "맑음", "", "구름많음", "흐림"]
    rain_type = ["", "비", "진눈깨비", "눈", "소나기"]

    # 날씨들 평균을 구해서 출력을 위한 함수
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

    # 아이템 for 문 돌리기
    for item in element_list:
        isPm = True
        idx = -1

        # category 태그와 fcstValue(예보 수치) 태그 찾기
        category = item.find('category').text
        fcstValue = item.find('fcstValue').text

        for i in range(len(dataset)):
            if dataset[i] == item.find('fcstDate').text:  # 해당 날짜 예보인지 확인 후 idx 변경
                idx = i

        if int(item.find('fcstTime').text) < 1200:  # 오전 예보인지 오후인지 확인
            isPm = False

        if category == "TMP":  # 기온 예보인 경우
            if dataset[idx].maxTemp < int(fcstValue):
                dataset[idx].maxTemp = int(fcstValue)
            if dataset[idx].minTemp > int(fcstValue):
                dataset[idx].minTemp = int(fcstValue)

        elif category == "POP":  # 강수 확률 예보인 경우
            if dataset[idx].rainProb < int(fcstValue):
                dataset[idx].rainProb = int(fcstValue)

        elif category == "SKY":  # 하늘 상태 예보인 경우
            time = 1 if isPm else 0
            weather[idx][time][int(fcstValue)] += 1  # 해당 타입 하늘 상태 개수 +1
            am_weather = 0
            pm_weather = 0

            # 하늘 상태 중 가장 많은 것을 해당 일자의 하늘 상태로 변경
            for i in range(5):
                if am_weather < weather[idx][0][i]:
                    am_weather = weather[idx][0][i]
                    dataset[idx].am_weather = sky_status[i]
                if pm_weather < weather[idx][1][i]:
                    pm_weather = weather[idx][1][i]
                    dataset[idx].pm_weather = sky_status[i]

        elif category == "PTY":  # 흐린 상태 예보인 경우
            if int(fcstValue) != 0 and not rain[idx][1 if isPm else 0]:
                if isPm:
                    dataset[idx].pm_weather = "흐리고 " + rain_type[int(fcstValue)]
                else:
                    dataset[idx].am_weather = "흐리고 " + rain_type[int(fcstValue)]

    return dataset


def middleXml2DataSet(element_list: list[xml.etree.ElementTree.Element], dataset: list[dataSet]):
    # 중기 예보 xml 형식 데이터를 dataSet 형식으로 변환

    # tElement: 기온 데이터, wElement: 날씨 데이터
    tElement = element_list[0]
    wElement = element_list[1]

    # 기온 데이터
    for i in range(len(tElement)):
        tag = tElement[i].tag  # 해당 태그 이름을 가져옴
        txt = tElement[i].text  # 해당 데이터를 가져옴

        if tag.find('ta') == -1 or tag.find('Low') != -1 or tag.find('High') != -1:  # 해당 태그가 기온 데이터가 아닌 경우
            continue  # 무시

        if int(tag[5]) < 3 or int(tag[5]) > 7:  # 3일 이전이나 7일 이후 데이터인 경우
            continue  # 무시

        if tag[:5] == "taMin":  # 해당 데이터가 최저 기온 데이터 인 경우
            dataset[int(tag[5])].minTemp = int(txt)

        elif tag[:5] == "taMax":  # 해당 데이터가 최고 기온 데이터 인 경우
            dataset[int(tag[5])].maxTemp = int(txt)

    # 날씨 데이터
    for i in range(len(wElement)):
        tag = wElement[i].tag
        txt = wElement[i].text

        if tag == 'regId' or not (tag.find('Am') != -1 or tag.find('Pm') != -1):  # 해당 태그가 날씨 데이터가 아닌 경우
            continue  # 무시
        if tag[:4] == 'rnSt':  # 강수 확률 데이터 인 경우
            if dataset[int(tag[4])].rainProb < int(txt):
                dataset[int(tag[4])].rainProb = int(txt)

        elif tag[:2] == 'wf':  # 날씨 예보 데이터 인 경우
            if tag.find('Am') != -1:
                dataset[int(tag[2])].am_weather = txt
            else:
                dataset[int(tag[2])].pm_weather = txt

    return dataset
