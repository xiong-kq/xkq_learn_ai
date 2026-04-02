# -*- encoding: UTF-8 -*-
# @autor: xkq
# @desc: 学习使用AI

import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.xkq_simple_ai import SimpleAi

parser = argparse.ArgumentParser(description="调用AI的程序入口")

parser.add_argument("-need_stream", default="N", help="是否需要流式输出，默认非流式输出(N:无需流式输出，Y:需要流式输出)")
parser.add_argument("-function_call", default="N", help="是否启用工具调用(Y:需要 N:不需要)")

args = parser.parse_args()

agent = SimpleAi(args)

agent.run()
