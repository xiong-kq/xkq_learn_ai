# -*- encoding: UTF-8 -*-
# @author: xkq
# @desc: 公共可用函数
import requests
import json

def get_weather_parase_data(city):
    """获取城市天气"""
    # 1. 获取指定城市经纬度
    latitude = 0
    longitude = 0
    search_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=4&language=zh"
    rsp = requests.request("GET", url=search_url)
    if rsp.status_code == 200:
        print(rsp.text)
        result = rsp.json().get("results")[0]
        latitude = result['latitude']
        longitude = result['longitude']
    # 2. 用经纬度查询当地天气
    forcast_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m,weather_code&daily=temperature_2m_max,temperature_2m_min&hourly=temperature_2m&forecast_days=3&timezone=Asia/Shanghai"
    forcast_rsp = requests.request("GET", url=forcast_url)
    if forcast_rsp.status_code == 200:
        current = forcast_rsp.json().get("current")
        current_temp = current.get("temperature_2m")
        current_wind_spped = current.get("wind_speed_10m")
        weather_code = current.get("weather_code")
        weather = weather_map(weather_code)
        daily_max_temp = max(forcast_rsp.json().get("hourly").get("temperature_2m"))
        daily_min_temp = min(forcast_rsp.json().get("hourly").get("temperature_2m"))
        temp_tomorrow_max = forcast_rsp.json().get("daily").get("temperature_2m_max")[1]
        temp_tomorrow_min = forcast_rsp.json().get("daily").get("temperature_2m_min")[1]
        return """{0}当前天气{7}, 气温为{1}摄氏度，风速为{2}km/h，最高温{3}摄氏度，最低温{4}摄氏度，
        未来一天最高温为{5}摄氏度，最低温为{6}摄氏度。
               """.format(city, current_temp, current_wind_spped,
                          daily_max_temp, daily_min_temp, temp_tomorrow_max,
                          temp_tomorrow_min, weather)

    return f"暂时没有获取到当前{city}城市的天气信息。"

def weather_map(weather_code):

    return {
            0: "晴朗",
            1: "主要晴",
            2: "局部多云",
            3: "阴天",
            45: "雾",
            48: "雾",
            51: "毛毛雨",
            53: "毛毛雨",
            55: "毛毛雨",
            61: "雨",
            63: "雨",
            65: "雨",
            71: "雪",
            73: "雪",
            75: "雪",
            80: "骤雨",
            81: "骤雨",
            82: "骤雨",
            95: "雷暴",
            96: "雷暴",
            99: "雷暴"
            }.get(weather_code)
