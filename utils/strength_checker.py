import string


def check_password_strength(password: str) -> str:
    """
    检测密码强度

    Args:
        password: 需要检测的密码

    Returns:
        密码强度等级：弱/中/强
    """
    score = 0
    has_digit = any(c in string.digits for c in password)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    type_count = sum([has_digit, has_lower, has_upper, has_special])
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    
    score += type_count
    
    if has_special:
        score += 1
    
    if score <= 2:
        return "弱"
    elif score <= 4:
        return "中"
    else:
        return "强"
