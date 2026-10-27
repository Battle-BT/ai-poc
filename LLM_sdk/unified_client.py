import os
from dotenv import load_dotenv
load_dotenv()                      # 读取.env文件里的key

from openai import OpenAI

#配置表： 厂商->地址+模型名
PROVIDERS = {
    "deepseek": {
        "base_url": "https://api.deepseek.cn/v1",
        "model": "ep-20261020132826-v6s6r",
    },
    "doubao": {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "model": "ep-20261020132826-v6s6r",
    },
    "qwen": {
        "base_url": "https://api.qwen.cn/v1",
        "model": "qwen-3.5",
    },
}


class UnifiedClient:
    def __init__(self,provider,api_key):
        cfg = PROVIDERS[provider]   #按厂商名获取配置
        self.client = OpenAI(
            api_key=api_key,
            base_url=cfg["base_url"]
        )
        self.model = cfg["model"]

    def chat(self, text):
        resp = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "user", "content": text}
            ]
        )
        return resp.choices[0].message.content
    
    def chat_stream(self, text):
        """流式输出：一个字一个字蹦出来"""
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": text}],
            stream=True
        )
        answer = ""
        for chunk in stream:                    # 一帧一帧收
            piece = chunk.choices[0].delta.content
            if piece:                           # 跳过空帧
                print(piece, end="", flush=True)
                answer += piece
        print()                                 # 收尾换行
        return answer

    

if __name__ == "__main__":
    # 验证：切换厂商只改一个参数，三家配置都打印出来
    for name in ["deepseek", "doubao", "qwen"]:
        c = UnifiedClient(name, "假key")
        print(name, "->", c.client.base_url, "|", c.model)