from unified_client import UnifiedClient
import os

# 用.env里的真key创建豆包客户端
c = UnifiedClient("doubao", os.getenv("ARK_API_KEY"))
print("当前模型:", c.model)
print("回答：")

answer = c.chat_stream("你是谁")
#print("完整回答:", answer)
