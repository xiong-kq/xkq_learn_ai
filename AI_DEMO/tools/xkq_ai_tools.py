# -*- encoding: UTF-8 -*-
# @author: xkq
# @desc: 工具模型
from pydantic import BaseModel, Field
from typing import List, Optional

class WeatherInput(BaseModel):
    city: str = Field(..., description="城市名称, 例如成都市,北京市")
    query_date: Optional[str] = Field(description="查询时间，例如今天，明天，未来一天")

class CurrentTime(BaseModel):
    current_date: Optional[str] = Field(description="获取当前时间, 例如，现在时间")