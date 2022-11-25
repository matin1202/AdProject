import traceback

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import data_set
import request


class MainUI(QWidget):
    def __init__(self):
        super().__init__()

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

        self.proverb = QLabel("여기에 격언 표시")
        self.proverb.setAlignment(Qt.AlignCenter)

        vBox2 = QGridLayout()
        self.label: list[MyLabel] = []

        for data in self.dataSet:
            if data == self.calendar.selectedDate().toString('yyyyMMdd'):
                self.label = [
                    MyLabel("평균 " + str(int((data.maxTemp + data.minTemp) / 2)) + "도"),
                    MyLabel("강수 확률 " + str(data.rainProb) + "%"),
                    MyLabel("최고 " + str(data.maxTemp) + "도"),
                    MyLabel("최저 " + str(data.minTemp) + "도"),
                    MyLabel("오전 " + str(data.am_weather)),
                    MyLabel("오후 " + str(data.pm_weather))
                ]

        for i in range(len(self.label)):
            vBox2.addWidget(self.label[i], i // 2, i % 2)

        vBox.addWidget(self.calendar)
        vBox.addWidget(self.proverb)
        hLayout.addLayout(vBox)
        hLayout.addLayout(vBox2)

        self.mainLayout.addLayout(hLayout)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("날씨 조회")

    def changed(self):
        date = self.calendar.selectedDate()
        label = []
        for data_ in self.dataSet:
            if data_ == self.calendar.selectedDate().toString('yyyyMMdd'):
                label = [
                    "평균 " + str(int((data_.maxTemp + data_.minTemp) / 2)) + "도",
                    "강수 확률 " + str(data_.rainProb) + "%",
                    "최고 " + str(data_.maxTemp) + "도",
                    "최저 " + str(data_.minTemp) + "도",
                    "오전 " + str(data_.am_weather),
                    "오후 " + str(data_.pm_weather)
                ]
        for la in range(len(label)):
            self.label[la].setText(label[la])


class MyLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(str(text))
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(QSize(120, 40))


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
