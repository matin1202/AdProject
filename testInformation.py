import random
import unittest

import data_set
import information
from PyQt5.QtCore import QDate


class testInformation(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testClothes(self):
        self.assertEqual(information.clothes(28), "cloth = 린넨 옷 \ntop = 민소매, 반팔 \nbottom = 반바지, 짧은 치마")

        self.assertEqual(information.clothes(23), "top = 반팔, 얇은 셔츠 \nbottom = 반바지, 면바지")

        self.assertEqual(information.clothes(20), "top = 블라우스, 긴팔 티\nbottom = 면바지, 슬랙스")

        self.assertEqual(information.clothes(17), "outer = 얇은 가디건\ntop = 니트, 맨투맨, 후드티\nbottom = 긴바지")

        self.assertEqual(information.clothes(12), "outer = 자켓, 가디건, 청자켓\ntop = 니트\nbottom = 스타킹, 청바지")

        self.assertEqual(information.clothes(9), "outer = 트렌치코트, 야상, 점퍼\nbottom = 스타킹, 기모바지")

        self.assertEqual(information.clothes(5), "cloth = 가죽 옷\nouter = 울 코트\netc = 히트텍, 기모")

        self.assertEqual(information.clothes(-28), "cloth = 누빔 옷\nouter = 패딩, 두꺼운 코트\netc = 기모, 목도리")

    def testEtc(self):
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
            if data.rainProb >= 65:
                self.assertEqual(information.etc(data), "우산을 챙기는 것을 추천드립니다.")
                continue
            temp = int((minTemp[i] + maxTemp[i]) / 2)
            if temp <= 5:
                self.assertEqual(information.etc(data), "핫팩, 장갑 등 방한용품을 챙기는 것을 추천드립니다.")
            elif temp >= 28:
                self.assertEqual(information.etc(data), "기온이 높으므로 선풍기, 부채 등을 챙기는 것을 추천드립니다.")
            else:
                self.assertEqual(information.etc(data), "특별한 추천 준비물이 없습니다.")
