import traceback

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # 이미지 넣기 위해

import data_set
import request
import phrase   # 명언 리스트
import information  # 옷차림, 준비물
import chooseimage  # 날씨 이미지


class MainUI(QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        self.dataSet: list[data_set.dataSet] = request.requestWeatherStatus()

        self.mainLayout = QHBoxLayout()

        hLayout = QHBoxLayout()

        vBox = QVBoxLayout()

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(False)

        today = QDate().currentDate()
        aWeekLater = QDate().currentDate().addDays(6)

        self.calendar.setDateRange(today, aWeekLater)
        self.calendar.selectionChanged.connect(self.changed)
        self.calendar.setFixedSize(QSize(400, 400))

        self.information = QTextEdit(self)  # 옷차림, 준비물 나타낼 곳
        self.information.setFixedSize(QSize(400, 200))

        vBox.addWidget(self.calendar)
        vBox.addWidget(self.information)

        vBox2 = QGridLayout()
        self.label: list[MyLabel] = []

        for data in self.dataSet:
            if data == self.calendar.selectedDate().toString('yyyyMMdd'):
                self.showInformation(data)
                self.label = [
                    MyImageLabel(chooseimage.chooseImg(data)),
                    MyLabel(phrase.randomPhrase()),
                    MyLabel("평균 " + str(int((data.maxTemp + data.minTemp) / 2)) + "도"),
                    MyLabel("강수 확률 " + str(data.rainProb) + "%"),
                    MyLabel("최고 " + str(data.maxTemp) + "도"),
                    MyLabel("최저 " + str(data.minTemp) + "도"),
                    MyLabel("오전 " + str(data.am_weather)),
                    MyLabel("오후 " + str(data.pm_weather))
                ]

        for i in range(len(self.label)):
            vBox2.addWidget(self.label[i], i // 2, i % 2)
        hLayout.addLayout(vBox)
        hLayout.addLayout(vBox2)

        self.mainLayout.addLayout(hLayout)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("날씨 조회")

    def changed(self):
        label = []
        for data_ in self.dataSet:
            if data_ == self.calendar.selectedDate().toString('yyyyMMdd'):
                self.showInformation(data_)
                label = [
                    chooseimage.chooseImg(data_),
                    phrase.randomPhrase(),
                    "평균 " + str(int((data_.maxTemp + data_.minTemp) / 2)) + "도",
                    "강수 확률 " + str(data_.rainProb) + "%",
                    "최고 " + str(data_.maxTemp) + "도",
                    "최저 " + str(data_.minTemp) + "도",
                    "오전 " + str(data_.am_weather),
                    "오후 " + str(data_.pm_weather)
                ]
        for la in range(len(label)):
            self.label[la].setText(label[la])

    def showInformation(self, data_: data_set.dataSet):
        self.information.clear()
        clothesInfo = "추천 옷차림: " + information.clothes(int((data_.maxTemp + data_.minTemp) / 2))     # 최고기온, 최저기온 평균내서 함수 매개변수로 집어넣기
        self.information.append(clothesInfo)
        etcInfo = "추천 준비물: " + information.etc(data_)    # 온도나 비, 눈 등에 따른 추천 준비물/ 온도, 강수확률을 매개변수로 넣기
        self.information.append(etcInfo)


class MyLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(str(text))
        self.setFont(QFont("나눔", 11))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(QSize(160, 160))
        self.setWordWrap(True)


class MyImageLabel(QLabel):

    def __init__(self, url, *__args):
        super().__init__(*__args)
        pixmap = QPixmap()
        pixmap.load(url)
        pixmap = pixmap.scaledToWidth(160)
        self.setPixmap(pixmap)
        self.setContentsMargins(10, 10, 10, 10)
        self.resize(pixmap.width(), pixmap.height())

    def setText(self, p_str):
        pixmap = QPixmap()
        pixmap.load(p_str)
        pixmap = pixmap.scaledToWidth(160)
        self.setPixmap(pixmap)
        self.setContentsMargins(10, 10, 10, 10)
        self.resize(pixmap.width(), pixmap.height())


def test():
    try:
        request.requestWeatherStatus()
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    import sys

    # test()

    app = QApplication(sys.argv)
    calc = MainUI()
    calc.show()
    sys.exit(app.exec_())
