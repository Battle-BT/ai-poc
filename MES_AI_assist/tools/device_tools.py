# device_tools.py - 设备管理工具
import os
import json

DATA_DIR = os.path.join(os.path.dirname(__file__),"..","data")
DEVICES_FILE = os.path.join(DATA_DIR,"devices.json")

def _load_devices():
    with open(DEVICES_FILE,"r",encoding="utf-8") as f:
        return json.load(f)["devices"]
    
def get_device_status(device_id):
    """查询指定设备的当前运行状态
    
    参数：
       device_id(str)：设备编号，如DEV-003

    返回：
       dict:设备状态信息
    """
    for d in _load_devices():
        if d["device_id"] == device_id:
            return {
                "device_id": d["device_id"],
                "name":d["name"],
                "status":d["status"],
                "fault":d["fault"]
            }
    return{"error":f"找不到设备{device_id}"}