import string


def check_password_strength(password: str) -> str:
    """检测密码强度

    Args:
        password: 待检测的密码字符串

    Returns:
        强度等级：弱/中/强
    """
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    has_digit = any(c in string.digits for c in password)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_special = any(c not in string.digits + string.ascii_letters for c in password)

    char_types = sum([has_digit, has_lower, has_upper, has_special])
    score += char_types

    if has_special:
        score += 1

    if score <= 2:
        return "弱"
    elif score <= 4:
        return "中"
    else:
        return "强"


def get_strength_score(password: str) -> int:
    """获取密码强度分数

    Args:
        password: 待检测的密码字符串

    Returns:
        强度分数（0-6）
    """
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    has_digit = any(c in string.digits for c in password)
    has_lower = any(c in string.ascii_lowercase for c in password)
    has_upper = any(c in string.ascii_uppercase for c in password)
    has_special = any(c not in string.digits + string.ascii_letters for c in password)

    char_types = sum([has_digit, has_lower, has_upper, has_special])
    score += char_types

    if has_special:
        score += 1

    return score
