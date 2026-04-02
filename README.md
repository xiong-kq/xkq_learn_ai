项目说明: 用于学习使用AI

项目结构: 

    bin - 程序入口

    config - 项目配置(api_key, model, base_url)

    core - 简单agent实现目录

    tools - agent可用的工具目录(实现了简单的获取当前时间，获取实时天气)

    utils - 辅助实现功能目录

使用方式:

```bash
    python xkq_llm_learn.py [参数可选 -stream(选择AI回答是否以流式输出Y是，N否) -function_call(选择是否让AI使用工具 Y是，N否) ]
```