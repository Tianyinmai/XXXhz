import random
import string
from typing import List

CONFUSING_CHARS = {'0', 'O', '1', 'l', 'I'}


def get_characters(use_digits: bool = True, use_lower: bool = True,
                   use_upper: bool = True, use_special: bool = True,
                   exclude_confusing: bool = False) -> str:
    """
    获取可选字符集合

    Args:
        use_digits: 是否使用数字
        use_lower: 是否使用小写字母
        use_upper: 是否使用大写字母
        use_special: 是否使用特殊符号
        exclude_confusing: 是否排除易混淆字符

    Returns:
        可选字符组成的字符串
    """
    chars = []
    if use_digits:
        chars.append(string.digits)
    if use_lower:
        chars.append(string.ascii_lowercase)
    if use_upper:
        chars.append(string.ascii_uppercase)
    if use_special:
        chars.append('!@#$%^&*()_+-=[]{}|;:,.<>?')
    
    all_chars = ''.join(chars)
    
    if exclude_confusing:
        all_chars = ''.join(c for c in all_chars if c not in CONFUSING_CHARS)
    
    return all_chars


def generate_single_password(length: int = 16, use_digits: bool = True,
                             use_lower: bool = True, use_upper: bool = True,
                             use_special: bool = True, exclude_confusing: bool = False) -> str:
    """
    生成单个随机密码

    Args:
        length: 密码长度（6-32）
        use_digits: 是否使用数字
        use_lower: 是否使用小写字母
        use_upper: 是否使用大写字母
        use_special: 是否使用特殊符号
        exclude_confusing: 是否排除易混淆字符

    Returns:
        生成的随机密码

    Raises:
        ValueError: 密码长度不在有效范围或未选择任何字符类型
    """
    if length < 6 or length > 32:
        raise ValueError("密码长度必须在6-32之间")
    
    chars = get_characters(use_digits, use_lower, use_upper, use_special, exclude_confusing)
    
    if not chars:
        raise ValueError("至少需要选择一种字符类型")
    
    password = []
    if use_digits:
        available = [c for c in string.digits if c not in (CONFUSING_CHARS if exclude_confusing else set())]
        if available:
            password.append(random.choice(available))
    
    if use_lower:
        available = [c for c in string.ascii_lowercase if c not in (CONFUSING_CHARS if exclude_confusing else set())]
        if available:
            password.append(random.choice(available))
    
    if use_upper:
        available = [c for c in string.ascii_uppercase if c not in (CONFUSING_CHARS if exclude_confusing else set())]
        if available:
            password.append(random.choice(available))
    
    if use_special:
        available = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        password.append(random.choice(available))
    
    remaining_length = length - len(password)
    if remaining_length > 0:
        password.extend(random.choice(chars) for _ in range(remaining_length))
    
    random.shuffle(password)
    return ''.join(password)


def generate_batch_passwords(count: int = 1, length: int = 16,
                             use_digits: bool = True, use_lower: bool = True,
                             use_upper: bool = True, use_special: bool = True,
                             exclude_confusing: bool = False) -> List[str]:
    """
    批量生成随机密码

    Args:
        count: 生成数量（1-100）
        length: 密码长度（6-32）
        use_digits: 是否使用数字
        use_lower: 是否使用小写字母
        use_upper: 是否使用大写字母
        use_special: 是否使用特殊符号
        exclude_confusing: 是否排除易混淆字符

    Returns:
        生成的密码列表

    Raises:
        ValueError: 生成数量不在有效范围
    """
    if count < 1 or count > 100:
        raise ValueError("批量生成数量必须在1-100之间")
    
    return [generate_single_password(length, use_digits, use_lower, use_upper, use_special, exclude_confusing)
            for _ in range(count)]
