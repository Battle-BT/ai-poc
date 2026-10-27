import time

# 模拟器：假装是API在流式吐字（每0.1秒吐一个字）
def mock_api_stream(text):
    for ch in text:
        yield {"choices": [{"delta": {"content": ch}}]}   # 模拟一帧
        time.sleep(0.1)                                   # 模拟生成速度

# 打字机效果
answer = ""
for chunk in mock_api_stream("你好，我是流式输出，看到我一个字一个字蹦出来了吗"):
    piece = chunk["choices"][0]["delta"]["content"]
    if piece:
        print(piece, end="", flush=True)   # flush=True强制立即显示
        answer += piece

print()
print("完整答案：", answer)
