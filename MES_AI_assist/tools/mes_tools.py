#mes_tools.py -MES派工工具
#职责：根据模组编号，从人员技能库找出做过该模组的工人，按匹配度排序返回推荐

import json
import os

#数据文件路径：data/workers.json
DATA_DIR = os.path.join(os.path.dirname(__file__),"..","data")
WORKERS_FILE = os.path.join(DATA_DIR,"workers.json")

def _load_workers():
    """读取人员技能库（模拟MES数据库）"""
    with open(WORKERS_FILE,"r",encoding="utf-8") as f:
        data = json.load(f)
    return data["workers"]

def recommend_workers(module_id):
    """
    根据模组编号推荐适合的工人
    参数：
       module_id(str):模组编号，如“MOD-003”
    返回：
       list[dict]: 推荐工人列表，按匹配度从高到低排序
    """
    workers = _load_workers()
    result = []
    for w in workers:
        exp = w.get("module_experience",{})
        if module_id in exp:
            result.append(
                {
                    "worker_id":w["worker_id"],
                    "name":w["name"],
                    "team":w["team"],
                    "skill_level":w["skill_level"],
                    "assembly_count":exp[module_id], #经验（做过几次）
                    "match_score":exp[module_id] * 2 + (1 if w["skill_level"] == "A" else 0)
                }
            )
    #匹配度从高到底排序
    result.sort(key=lambda x:x["match_score"],reverse = True)
    return result

