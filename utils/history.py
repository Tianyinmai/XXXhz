import json
import os
from datetime import datetime
from typing import List

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'passwords.json')


def save_passwords_history(passwords: List[str], strengths: List[str]) -> None:
    """
    保存密码历史记录到本地文件

    Args:
        passwords: 生成的密码列表
        strengths: 对应的密码强度列表
    """
    history = {
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "密码列表": passwords,
        "强度": strengths
    }
    
    existing_data = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    data = json.loads(content)
                    if isinstance(data, list):
                        existing_data = data
                    else:
                        existing_data = [data]
        except (json.JSONDecodeError, IOError):
            pass
    
    existing_data.append(history)
    
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)


def load_history() -> List[dict]:
    """
    加载历史记录

    Returns:
        历史记录列表
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.strip():
                data = json.loads(content)
                if isinstance(data, list):
                    return data
                else:
                    return [data]
    except (json.JSONDecodeError, IOError):
        pass
    
    return []


def clear_history() -> bool:
    """
    清空历史记录

    Returns:
        成功返回True，失败返回False
    """
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True
    except IOError:
        return False
