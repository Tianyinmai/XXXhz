import string
from typing import Tuple


class StrengthChecker:
    """密码强度检测类"""
    
    @staticmethod
    def check(password: str) -> Tuple[str, int]:
        """
        检测密码强度
        
        Args:
            password: 待检测的密码字符串
            
        Returns:
            元组：(强度等级, 分数)
            强度等级：弱/中/强
            分数：0-100
        """
        score = 0
        
        if len(password) >= 6:
            score += 10
        if len(password) >= 8:
            score += 10
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        has_digit = any(c in string.digits for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        type_count = sum([has_digit, has_lower, has_upper, has_special])
        
        if type_count == 1:
            score += 10
        elif type_count == 2:
            score += 25
        elif type_count == 3:
            score += 40
        elif type_count == 4:
            score += 50
        
        if has_digit and has_lower:
            score += 5
        if has_digit and has_upper:
            score += 5
        if has_lower and has_upper:
            score += 5
        if has_special:
            score += 10
        
        unique_chars = len(set(password))
        if unique_chars >= len(password) * 0.8:
            score += 10
        
        if score < 40:
            strength = "弱"
        elif score < 70:
            strength = "中"
        else:
            strength = "强"
        
        return strength, min(score, 100)
    
    @staticmethod
    def get_strength_tips(password: str) -> list:
        """
        获取密码强度改进建议
        
        Args:
            password: 待检测的密码字符串
            
        Returns:
            改进建议列表
        """
        tips = []
        
        if len(password) < 8:
            tips.append("建议密码长度至少8位")
        if len(password) < 12:
            tips.append("建议密码长度至少12位以获得更高安全性")
        
        if not any(c in string.digits for c in password):
            tips.append("建议添加数字")
        if not any(c in string.ascii_lowercase for c in password):
            tips.append("建议添加小写字母")
        if not any(c in string.ascii_uppercase for c in password):
            tips.append("建议添加大写字母")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            tips.append("建议添加特殊符号")
        
        return tips
