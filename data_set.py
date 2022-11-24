import xml.etree.ElementTree

from PyQt5.QtCore import QDate


class dataSet:
    def __init__(self, date: QDate, isPm: bool, minTemp: int, maxTemp, weather: str):
        self.date = date
        self.isPm = isPm
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.weather = weather

    def __str__(self):
        return self.date.toString('yyyy년 MM월 dd일 ') + ("오후" if self.isPm else "오전") + "\n"\
               + "최고 온도 : " + str(self.maxTemp) + ", 최저 온도 : " + str(self.minTemp)\
               + ", 날씨 : " + self.weather


def middleXml2DataSet(element_list: list[xml.etree.ElementTree.Element]):
    tElement = element_list[0]
    wElement = element_list[1]
