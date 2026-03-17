"""
密码生成器核心模块
提供密码生成、批量生成、历史记录保存等功能
"""

import random
import string
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class PasswordGenerator:
    """密码生成器类"""
    
    # 字符集定义
    DIGITS = string.digits  # 数字
    LOWERCASE = string.ascii_lowercase  # 小写字母
    UPPERCASE = string.ascii_uppercase  # 大写字母
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # 特殊符号
    
    # 易混淆字符映射
    CONFUSING_CHARS = {
        '0': 'O', 'O': '0',
        '1': 'l', 'l': '1',
        'I': '1', '1': 'I'
    }
    
    def __init__(self, history_file: str = "passwords.json"):
        """
        初始化密码生成器
        
        Args:
            history_file: 历史记录文件路径
        """
        self.history_file = history_file
        self._ensure_history_file()
    
    def _ensure_history_file(self) -> None:
        """确保历史记录文件存在"""
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _get_character_set(
        self,
        use_digits: bool = True,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_special: bool = False,
        exclude_confusing: bool = False
    ) -> str:
        """
        根据选项获取字符集
        
        Args:
            use_digits: 是否包含数字
            use_lowercase: 是否包含小写字母
            use_uppercase: 是否包含大写字母
            use_special: 是否包含特殊符号
            exclude_confusing: 是否排除易混淆字符
            
        Returns:
            可用的字符集字符串
        """
        charset = ""
        
        if use_digits:
            charset += self.DIGITS
        if use_lowercase:
            charset += self.LOWERCASE
        if use_uppercase:
            charset += self.UPPERCASE
        if use_special:
            charset += self.SPECIAL
        
        # 排除易混淆字符
        if exclude_confusing:
            confusing = set('0O1lI')
            charset = ''.join(c for c in charset if c not in confusing)
        
        return charset
    
    def generate(
        self,
        length: int = 16,
        use_digits: bool = True,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_special: bool = False,
        exclude_confusing: bool = False
    ) -> str:
        """
        生成单个密码
        
        Args:
            length: 密码长度（6-32位）
            use_digits: 是否包含数字
            use_lowercase: 是否包含小写字母
            use_uppercase: 是否包含大写字母
            use_special: 是否包含特殊符号
            exclude_confusing: 是否排除易混淆字符
            
        Returns:
            生成的密码字符串
            
        Raises:
            ValueError: 当参数不合法时抛出
        """
        # 参数验证
        if not 6 <= length <= 32:
            raise ValueError(f"密码长度必须在6-32位之间，当前: {length}")
        
        # 获取字符集
        charset = self._get_character_set(
            use_digits, use_lowercase, use_uppercase, use_special, exclude_confusing
        )
        
        if not charset:
            raise ValueError("至少需要选择一种字符类型")
        
        # 生成密码
        password = ''.join(random.choice(charset) for _ in range(length))
        
        return password
    
    def generate_batch(
        self,
        count: int = 1,
        length: int = 16,
        use_digits: bool = True,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_special: bool = False,
        exclude_confusing: bool = False
    ) -> List[str]:
        """
        批量生成密码
        
        Args:
            count: 生成数量（1-100）
            length: 密码长度（6-32位）
            use_digits: 是否包含数字
            use_lowercase: 是否包含小写字母
            use_uppercase: 是否包含大写字母
            use_special: 是否包含特殊符号
            exclude_confusing: 是否排除易混淆字符
            
        Returns:
            生成的密码列表
            
        Raises:
            ValueError: 当参数不合法时抛出
        """
        if not 1 <= count <= 100:
            raise ValueError(f"批量生成数量必须在1-100之间，当前: {count}")
        
        passwords = []
        for _ in range(count):
            pwd = self.generate(
                length, use_digits, use_lowercase, use_uppercase, use_special, exclude_confusing
            )
            passwords.append(pwd)
        
        return passwords
    
    def save_to_history(
        self,
        passwords: List[str],
        strengths: List[str]
    ) -> None:
        """
        保存生成记录到历史文件
        
        Args:
            passwords: 生成的密码列表
            strengths: 对应的密码强度列表
        """
        record = {
            "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "密码列表": passwords,
            "强度": strengths
        }
        
        # 读取现有历史
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            history = []
        
        # 添加新记录
        history.append(record)
        
        # 保存
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def get_history(self) -> List[Dict]:
        """
        获取所有历史记录
        
        Returns:
            历史记录列表
        """
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def clear_history(self) -> bool:
        """
        清空历史记录
        
        Returns:
            是否成功清空
        """
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
