import data_set


def chooseImg(data_: data_set.dataSet) -> str:
    weather = [data_.am_weather, data_.pm_weather]
    if "흐리고 눈" in weather or "눈" in weather:
        return "images/snowy.png"
    elif "흐리고 진눈깨비" in weather or "진눈깨비" in weather:
        return "images/sleet.png"
    elif "흐리고 소나기" in weather or "소나기" in weather:
        return "images/shower.png"
    elif "흐리고 비" in weather:
        return "images/rainy.png"
    elif "흐림" in weather:
        return "images/groomy.png"
    elif "구름많음" in weather:
        return "images/cloudy.png"
    elif "맑음" in weather:
        return "images/sunny.png"
    return "images/sunny.png"
