import traceback

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import request


class MainUI(QWidget):
    def __init__(self):
        super().__init__()

        self.shortWeather = request.requestShortWeather()
        self.longWeather = request

        self.mainLayout = QVBoxLayout()

        hBox = QHBoxLayout()

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(False)

        today = QDate.currentDate()
        aWeekLater = QDate.currentDate().addDays(6)

        self.calendar.setDateRange(today, aWeekLater)
        self.calendar.selectionChanged.connect(self.getDate)

        hBox.addWidget(self.calendar)
        self.mainLayout.addLayout(hBox)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("날씨 조회")

    def getDate(self):
        try:
            request.requestShortWeather(self.calendar.selectedDate())
        except:
            print(traceback.format_exc())


def getItems(items):
    result = []
    for i in items[:]:
        if i.find('fcstDate').text == date.toString('yyyyMMdd'):
            result.append(i)


def test():
    try:
        request.requestWeatherStatus()
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
    import sys

    test()

    #app = QApplication(sys.argv)
    #calc = MainUI()
    #calc.show()
    #sys.exit(app.exec_())
