import random
import string
from datetime import datetime
from typing import List, Tuple


class PasswordGenerator:
    """随机密码生成器类"""
    
    DIGITS = string.digits
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    CONFUSING_CHARS = {'0', 'O', '1', 'l', 'I'}
    
    def __init__(self):
        self.char_sets = {
            'digits': self.DIGITS,
            'lowercase': self.LOWERCASE,
            'uppercase': self.UPPERCASE,
            'special': self.SPECIAL
        }
    
    def _remove_confusing_chars(self, char_set: str) -> str:
        """
        从字符集中移除易混淆字符
        
        Args:
            char_set: 原始字符集字符串
            
        Returns:
            移除易混淆字符后的字符集字符串
        """
        return ''.join(c for c in char_set if c not in self.CONFUSING_CHARS)
    
    def _get_available_chars(self, char_types: List[int], exclude_confusing: bool = False) -> str:
        """
        根据选择的字符类型获取可用字符集
        
        Args:
            char_types: 字符类型列表，1=数字，2=小写字母，3=大写字母，4=特殊符号
            exclude_confusing: 是否排除易混淆字符
            
        Returns:
            可用字符集字符串
        """
        type_mapping = {
            1: 'digits',
            2: 'lowercase',
            3: 'uppercase',
            4: 'special'
        }
        
        available_chars = ''
        for char_type in char_types:
            if char_type in type_mapping:
                char_set = self.char_sets[type_mapping[char_type]]
                if exclude_confusing:
                    char_set = self._remove_confusing_chars(char_set)
                available_chars += char_set
        
        return available_chars
    
    def generate_password(self, length: int = 16, char_types: List[int] = None, 
                          exclude_confusing: bool = False) -> str:
        """
        生成单个随机密码
        
        Args:
            length: 密码长度，默认16位
            char_types: 字符类型列表，默认包含所有类型
            exclude_confusing: 是否排除易混淆字符，默认False
            
        Returns:
            生成的密码字符串
            
        Raises:
            ValueError: 当密码长度不在6-32范围内时抛出
        """
        if length < 6 or length > 32:
            raise ValueError("密码长度必须在6-32位之间")
        
        if char_types is None:
            char_types = [1, 2, 3, 4]
        
        if not char_types:
            raise ValueError("至少需要选择一种字符类型")
        
        available_chars = self._get_available_chars(char_types, exclude_confusing)
        
        if not available_chars:
            raise ValueError("排除易混淆字符后没有可用字符，请选择其他字符类型")
        
        password = ''.join(random.choices(available_chars, k=length))
        return password
    
    def generate_batch(self, count: int = 1, length: int = 16, 
                       char_types: List[int] = None, 
                       exclude_confusing: bool = False) -> List[str]:
        """
        批量生成密码
        
        Args:
            count: 生成数量，默认1个
            length: 密码长度，默认16位
            char_types: 字符类型列表
            exclude_confusing: 是否排除易混淆字符
            
        Returns:
            密码列表
            
        Raises:
            ValueError: 当生成数量不在1-100范围内时抛出
        """
        if count < 1 or count > 100:
            raise ValueError("批量生成数量必须在1-100之间")
        
        passwords = []
        for _ in range(count):
            password = self.generate_password(length, char_types, exclude_confusing)
            passwords.append(password)
        
        return passwords
