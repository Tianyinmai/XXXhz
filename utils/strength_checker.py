"""
密码强度检测模块
提供密码强度评估功能
"""

import re
from typing import Dict


class StrengthChecker:
    """密码强度检测器类"""
    
    # 强度等级定义
    WEAK = "弱"
    MEDIUM = "中"
    STRONG = "强"
    
    def __init__(self):
        """初始化强度检测器"""
        pass
    
    def check(self, password: str) -> str:
        """
        检测密码强度
        
        评分标准：
        - 长度 >= 8: +1分
        - 长度 >= 12: +1分
        - 包含数字: +1分
        - 包含小写字母: +1分
        - 包含大写字母: +1分
        - 包含特殊符号: +1分
        
        强度等级：
        - 0-2分: 弱
        - 3-4分: 中
        - 5分以上: 强
        
        Args:
            password: 待检测的密码
            
        Returns:
            密码强度等级（"弱"/"中"/"强"）
        """
        if not password:
            return self.WEAK
        
        score = 0
        
        # 长度评分
        length = len(password)
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        
        # 字符类型评分
        if re.search(r'\d', password):  # 数字
            score += 1
        if re.search(r'[a-z]', password):  # 小写字母
            score += 1
        if re.search(r'[A-Z]', password):  # 大写字母
            score += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):  # 特殊符号
            score += 1
        
        # 判定强度等级
        if score <= 2:
            return self.WEAK
        elif score <= 4:
            return self.MEDIUM
        else:
            return self.STRONG
    
    def check_batch(self, passwords: list) -> list:
        """
        批量检测密码强度
        
        Args:
            passwords: 密码列表
            
        Returns:
            对应的强度等级列表
        """
        return [self.check(pwd) for pwd in passwords]
    
    def get_detailed_analysis(self, password: str) -> Dict:
        """
        获取密码的详细分析报告
        
        Args:
            password: 待检测的密码
            
        Returns:
            包含详细分析信息的字典
        """
        analysis = {
            "password": password,
            "length": len(password),
            "has_digits": bool(re.search(r'\d', password)),
            "has_lowercase": bool(re.search(r'[a-z]', password)),
            "has_uppercase": bool(re.search(r'[A-Z]', password)),
            "has_special": bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
            "strength": self.check(password)
        }
        
        # 计算得分
        score = 0
        if analysis["length"] >= 8:
            score += 1
        if analysis["length"] >= 12:
            score += 1
        if analysis["has_digits"]:
            score += 1
        if analysis["has_lowercase"]:
            score += 1
        if analysis["has_uppercase"]:
            score += 1
        if analysis["has_special"]:
            score += 1
        
        analysis["score"] = score
        analysis["max_score"] = 6
        
        return analysis
