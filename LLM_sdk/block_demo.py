import asyncio, time

async def 甲():
    print("甲：开始")
    await asyncio.sleep(3)      # ❌ 普通time.sleep，模拟CPU密集计算（占住线程不放手）
    print("甲：完成")

async def 乙():
    print("乙：开始")
    await asyncio.sleep(2)
    print("乙：完成")

async def main():
    await asyncio.gather(甲(), 乙())

asyncio.run(main())
