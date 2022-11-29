import unittest
import random

import data_set
import chooseimage

from PyQt5.QtCore import QDate


class testChooseImage(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testChooseImage(self):
        weathers = ["맑음", "구름많음", "흐림", "흐리고 비", "흐리고 진눈깨비", "흐리고 눈", "흐리고 소나기"]
        minTemp = [random.randrange(-30, 0) for _ in range(100)]
        maxTemp = [random.randrange(1, 30) for _ in range(100)]
        am_weather = [random.choice(weathers) for _ in range(100)]
        pm_weather = [random.choice(weathers) for _ in range(100)]
        rain_probs = [random.randrange(0, 100) for _ in range(100)]
        dataSets = [data_set.dataSet(QDate.currentDate(), minTemp[i], maxTemp[i], am_weather[i], pm_weather[i],
                                     rain_probs[i]) for i in range(100)]

        for i in range(100):
            data = dataSets[i]
            if data.pm_weather == "흐리고 눈" or data.am_weather == "흐리고 눈":
                self.assertEqual(chooseimage.chooseImg(data), "images/snowy.png")
                continue
            elif data.pm_weather == "흐리고 진눈깨비" or data.am_weather == "흐리고 진눈깨비":
                self.assertEqual(chooseimage.chooseImg(data), "images/sleet.png")
                continue
            elif data.pm_weather == "흐리고 소나기" or data.am_weather == "흐리고 소나기":
                self.assertEqual(chooseimage.chooseImg(data), "images/shower.png")
                continue
            elif data.pm_weather == "흐리고 비" or data.am_weather == "흐리고 비":
                self.assertEqual(chooseimage.chooseImg(data), "images/rainy.png")
                continue
            elif data.pm_weather == "흐림" or data.am_weather == "흐림":
                self.assertEqual(chooseimage.chooseImg(data), "images/groomy.png")
                continue
            elif data.pm_weather == "구름많음" or data.am_weather == "구름많음":
                self.assertEqual(chooseimage.chooseImg(data), "images/cloudy.png")
                continue
            elif data.pm_weather == "맑음" or data.am_weather == "맑음":
                self.assertEqual(chooseimage.chooseImg(data), "images/sunny.png")
