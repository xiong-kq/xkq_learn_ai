# -*- encoding: UTF-8 -*-
# @author: xkq
# @desc: AI对话处理
import json
import os
import sys

from openai import OpenAI
from dotenv import load_dotenv
from tools.ai_tools import tools
from utils.xkq_common_func import get_weather_parase_data
from datetime import datetime

env_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'ai_env.ini')
load_dotenv(dotenv_path=env_path)

class SimpleAi(object):
    def __init__(self, args):
        if args.need_stream.upper() == "Y":
            self.__need_stream = True
        else:
            self.__need_stream = False
        if args.function_call.upper() == "Y":
            self.__funciton_call = True
        else:
            self.__funciton_call = False
        self.__api_key = os.getenv("AI_API_KEY")
        self.__base_url = os.getenv("AI_BASE_URL")
        self.__model = os.getenv("AI_API_MODEL")
        if not ((self.__api_key != "" and self.__api_key is not None)
                and (self.__base_url != "" and self.__base_url is not None) and
                (self.__model != "" and self.__model is not None)):
             print("请检查[api_key, ai_base_url, model]配置是否已配置.")
             sys.exit(0)
        self.conversion_history = []
        self.llm = OpenAI(base_url=self.__base_url, api_key=self.__api_key)
        self.prompt = "你是一个风趣幽默的AI助手，回答用户热情友好并且积极，擅长使用表情，对于不知道的事情，直接说不知道。"

    def think(self, question):
        """AI处理问题"""
        # 保留最近几轮对话
        if len(self.conversion_history) > 10:
            self.conversion_history = self.conversion_history[-10:]
        full_content = ""
        messages = [{'role': 'system', 'content': self.prompt}]
        self.conversion_history.append(
                    {'role': 'user', 'content': question})
        messages.extend(self.conversion_history)
        if self.__funciton_call:
            response = self.llm.chat.completions.create(messages=messages, 
                                                        model=self.__model, 
                                                        temperature=0.7, 
                                                        stream=False,
                                                        tools=tools,
                                                        tool_choice='auto')
            msg = response.choices[0].message
            if msg.tool_calls:
                print(f"[系统] 检测到需要调用函数.")
                messages.append(msg)

                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    result = exec_func(func_name, func_args)
                    messages.append({'role': 'tool', "tool_call_id": tool_call.id, 'content': result})

        rsp_stream = self.llm.chat.completions.create(messages=messages, 
                                                    model=self.__model, 
                                                    temperature=0.7, 
                                                    stream=self.__need_stream)
        if not self.__need_stream:
            full_content = rsp_stream.choices[0].message.content
            print(f"AI助手: {full_content}")
        else:
            # 使用者采用流式输出
            print("AI助手: ", end="")
            for chunk in rsp_stream:
                if chunk.choices[0] and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_content += content

        self.conversion_history.append({'role': 'assistant', 'content': f'{full_content}'})
    
    def run(self):
        """启动函数"""
        while True:
            print("\n用户: ")
            user_input = input()
            if user_input.lower() in ["quit", 'exit', '退出']:
                print("AI助手: 再见！")
                break
            if user_input.strip() != "":
                self.think(question=user_input)


def get_weather(city, query_date=""):
    """获取天气信息"""
    return get_weather_parase_data(city=city)

def get_current_time():
    return f"当前时间为{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"

def exec_func(fn, args):
    if fn == "get_weather":
        return get_weather(**args)
    elif fn == "get_current_time":
        return get_current_time()
    else:
        return "未知函数"
        