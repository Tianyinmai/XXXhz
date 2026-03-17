import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "passwords.json")


def save_to_history(passwords: list, strengths: list) -> None:
    """保存密码到历史记录文件

    Args:
        passwords: 密码列表
        strengths: 强度列表
    """
    history = {
        "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "密码列表": passwords,
        "强度": strengths
    }

    existing_history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    existing_history = json.loads(content)
                    if isinstance(existing_history, dict):
                        existing_history = [existing_history]
        except (json.JSONDecodeError, IOError):
            existing_history = []

    if not isinstance(existing_history, list):
        existing_history = []

    existing_history.append(history)

    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_history, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"保存历史记录失败：{e}")


def load_history() -> list:
    """加载历史记录

    Returns:
        历史记录列表
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if content:
                history = json.loads(content)
                if isinstance(history, dict):
                    return [history]
                return history if isinstance(history, list) else []
    except (json.JSONDecodeError, IOError):
        pass

    return []
