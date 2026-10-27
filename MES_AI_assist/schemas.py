# schemas.py - 所有函数的JSON说明
# 职责：告诉LLM“有哪些工具可用、每个工具要什么参数”
# 注意：name必须和tools/里的Python函数名一摸一样！

ALL_TOOLS = [
    {
        "type":"function",
        "function":{
            "name":"recommend_workers",
            "description":"根据模组编号，推荐有该模组装配经验的工人，按匹配度排序返回。用于MES派工辅助。",
            "parameters":{
                "type":"object",
                "properties":{
                    "module_id":{
                        "type":"string",
                        "description":"模组编号，如MOD-003"
                    }
                },
                "required":["module_id"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_device_status",
            "description":"根据设备编号，查询该设备的当前运行状态。用于MES设备管理。",
            "parameters":{
                "type":"object",
                "properties":{
                    "device_id":{
                        "type":"string",
                        "description":"设备编号，如DEV-003"
                    }
                },
                "required":["device_id"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"query_fault_history",
            "description":"根据故障现象关键词，查询历史故障记录和解决措施。用于MES故障管理。",
            "parameters":{
                "type":"object",
                "properties":{
                    "symptom":{
                        "type":"string",
                        "description":"故障现象关键词，如 电机过热"
                    }
                },
                "required":["symptom"]
            }
        }
    }

]