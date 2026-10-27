# fault_tools.py —— 异常历史查询工具（需求1）
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FAULTS_FILE = os.path.join(DATA_DIR, "fault_history.json")


def _load_faults():
    with open(FAULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["faults"]


def query_fault_history(symptom):
    """
    根据故障现象关键词，查询历史故障记录和解决措施。

    参数:
        symptom (str): 故障现象关键词，如 电机过热

    返回:
        list[dict]: 相关历史记录列表
    """
    result = []
    for f in _load_faults():
        if symptom in f["symptom"]:        # 模糊匹配：现象里包含关键词
            result.append({
                "fault_id": f["fault_id"],
                "device_id": f["device_id"],
                "symptom": f["symptom"],
                "cause": f["cause"],
                "solution": f["solution"],
                "date": f["date"]
            })
    return result if result else {"message": f"未找到'{symptom}'相关历史记录"}
