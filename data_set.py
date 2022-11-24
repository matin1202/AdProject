import xml.etree.ElementTree

from PyQt5.QtCore import QDate


class dataSet:
    def __init__(self, date: QDate = QDate.currentDate(), avgTemp: int = 0, minTemp: int = 0, maxTemp: int = 0,
                 am_weather: str = "Unknown", pm_weather: str = "Unknown", rainProb: int = 0) -> None:
        self.date = date
        self.avgTemp = avgTemp
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.am_weather = am_weather
        self.pm_weather = pm_weather
        self.rainProb = rainProb

    def __str__(self):
        return self.date.toString('yyyy년 MM월 dd일 ') + "평균 기온 : " + str(self.avgTemp) \
               + ", 최저 온도 : " + str(self.minTemp) + ", 최고 온도 : " + str(self.maxTemp)\
               + ", 오전 날씨 : " + self.am_weather + ", 오후 날씨 : " + self.pm_weather\
               + ", 강수 확률 : " + str(self.rainProb) + "%"


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
            dataset[int(tag[5])].avgTemp = int((dataset[int(tag[5])].minTemp + dataset[int(tag[5])].maxTemp) / 2)
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
