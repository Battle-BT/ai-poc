# main.py - 入口：命令行与AI对话
from assistant import run

if __name__ == "__main__":
    question = input("你：")
    answer = run(question)
    print("AI:",answer)