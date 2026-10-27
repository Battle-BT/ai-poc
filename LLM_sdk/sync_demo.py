import time, os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY"),
)

def ask_sync(i):
    resp = client.chat.completions.create(
        model="ep-20261020132826-v6s6r",   
        messages=[{"role": "user", "content": f"用一句话回答：{i}乘以{i}等于多少？"}],
    )
    return resp.choices[0].message.content

start = time.time()
results = [ask_sync(i) for i in range(1, 6)]   # 串行：等完一个发一个
print(f"同步 5个请求耗时: {time.time()-start:.1f} 秒")
for r in results:
    print(" ", r)
