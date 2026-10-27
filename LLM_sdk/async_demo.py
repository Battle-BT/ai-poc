import asyncio, time, os
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

client = AsyncOpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.getenv("ARK_API_KEY"),
)
sem = asyncio.Semaphore(2)

async def ask(i):
    async with sem:
        resp = await client.chat.completions.create(
            model="ep-20261020132826-v6s6r",   
            messages=[{"role": "user", "content": f"用一句话回答：{i}乘以{i}等于多少？"}],
        )
        return resp.choices[0].message.content

async def main():
    start = time.time()
    results = await asyncio.gather(*[ask(i) for i in range(1, 6)])   # 并发：一起发
    print(f"异步 5个请求耗时: {time.time()-start:.1f} 秒")
    for r in results:
        print(" ", r)

asyncio.run(main())
