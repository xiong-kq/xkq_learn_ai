# -*- encoding: UTF-8 -*-
# @author: xkq
# @desc: 工具详情组装
import json

from .xkq_ai_tools import CurrentTime, WeatherInput

weather_schema = WeatherInput.model_json_schema()
time_schema = CurrentTime.model_json_schema()

tools = [
    {
        "type": 'function',
        "function": {
            "name": "get_weather",
            "description": "获取指定城市当前天气",
            "parameters": weather_schema
        }
    },
    {
        "type": 'function',
        "function": {
            "name": "get_current_time",
            "description": "获取当前的时间",
            "parameters": time_schema
        }
    }
]
