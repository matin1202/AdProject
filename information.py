import data_set


def clothes(temperature):
    if temperature >= 28:
        return "cloth = 린넨 옷 \ntop = 민소매, 반팔 \nbottom = 반바지, 짧은 치마"
    elif temperature >= 23:
        return "top = 반팔, 얇은 셔츠 \nbottom = 반바지, 면바지"
    elif temperature >= 20:
        return "top = 블라우스, 긴팔 티\nbottom = 면바지, 슬랙스"
    elif temperature >= 17:
        return "outer = 얇은 가디건\ntop = 니트, 맨투맨, 후드티\nbottom = 긴바지"
    elif temperature >= 12:
        return "outer = 자켓, 가디건, 청자켓\ntop = 니트\nbottom = 스타킹, 청바지"
    elif temperature >= 9:
        return "outer = 트렌치코트, 야상, 점퍼\nbottom = 스타킹, 기모바지"
    elif temperature >= 5:
        return "cloth = 가죽 옷\nouter = 울 코트\netc = 히트텍, 기모"
    else:
        return "cloth = 누빔 옷\nouter = 패딩, 두꺼운 코트\netc = 기모, 목도리"


def etc(weather: data_set.dataSet):
    temp = int((weather.minTemp + weather.maxTemp) / 2)
    if weather.rainProb >= 65:
        return "우산을 챙기는 것을 추천드립니다."
    if temp <= 5:
        return "핫팩, 장갑 등 방한용품을 챙기는 것을 추천드립니다."
    elif temp >= 28:
        return "기온이 높으므로 선풍기, 부채 등을 챙기는 것을 추천드립니다."
    return "특별한 추천 준비물이 없습니다."
