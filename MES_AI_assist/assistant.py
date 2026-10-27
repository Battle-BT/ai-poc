# assistant.py - 链路引擎/传话员
# 职责：收到问题->带说明书问LLM->要不要调用函数->真执行->回传给LLM->生成最终回答

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from schemas import ALL_TOOLS
from tools.mes_tools import recommend_workers
from tools.device_tools import get_device_status
from tools.fault_tools import query_fault_history

#1、读.env文件里的KEY
load_dotenv()

#2、初始化客户端（OpenAI兼容模式，火山方舟）
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)
MODEL = "ep-20261020132826-v6s6r"

#3、函数名->真函数 的映射表
AVAILABLE_FUNCTIONS = {
    "recommend_workers":recommend_workers,
    "get_device_status":get_device_status,
    "query_fault_history": query_fault_history,
}

def run(question):
    """处理用户问题，返回最终回答。"""
    messages = [
        {
            "role":"system","content":"你是MES系统助手。需要查数据时可以调用工具，回答问题优先查询问题是否符合真实运行情况，如果不符合，说明不符合真实情况，另外给出假设出现此类情况如何处理。"
        },
        {
            "role":"user","content":question
        }
    ]

    #  第一次调用：带说明书问LLM，看需不需要调用函数
    resp = client.chat.completions.create(
        model = MODEL,
        messages = messages,
        tools = ALL_TOOLS
    )
    msg = resp.choices[0].message

    # 判断：LLM要不要调用函数
    if msg.tool_calls:
        messages.append(msg)  # 1、把“我要调函数”加进上下文

        for tool_call in msg.tool_calls:  # LLM可能要调用多个函数，逐个处理
            func_name = tool_call.function.name  # LLM说的函数名
            arguments = json.loads(tool_call.function.arguments) # 解析参数

            # 2、从映射表查真函数，真执行
            func = AVAILABLE_FUNCTIONS[func_name]
            result = func(**arguments)

            # 3、结果作为tool消息回传，id对应上
            messages.append(
                {
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":json.dumps(result,ensure_ascii=False)
                }
            )
        
        # 第2次调用：把结果给LLM，让它组织成最终回答
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=ALL_TOOLS
        )

    return resp.choices[0].message.content
