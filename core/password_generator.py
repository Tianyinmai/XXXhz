import random
import string

CONFUSING_CHARS = {'0', 'O', '1', 'l', 'I'}


def generate_single_password(length: int = 16, use_digits: bool = True,
                             use_lower: bool = True, use_upper: bool = True,
                             use_special: bool = True, exclude_confusing: bool = False) -> str:
    """生成单个随机密码

    Args:
        length: 密码长度，默认为16，范围6-32
        use_digits: 是否使用数字，默认为True
        use_lower: 是否使用小写字母，默认为True
        use_upper: 是否使用大写字母，默认为True
        use_special: 是否使用特殊符号，默认为True
        exclude_confusing: 是否排除易混淆字符，默认为False

    Returns:
        生成的随机密码字符串

    Raises:
        ValueError: 当密码长度不在6-32范围内时抛出
        ValueError: 当未选择任何字符类型时抛出
    """
    if length < 6 or length > 32:
        raise ValueError("密码长度必须在6-32之间")

    char_sets = []
    if use_digits:
        char_sets.append(string.digits)
    if use_lower:
        char_sets.append(string.ascii_lowercase)
    if use_upper:
        char_sets.append(string.ascii_uppercase)
    if use_special:
        char_sets.append('!@#$%^&*()_+-=[]{}|;:,.<>?')

    if not char_sets:
        raise ValueError("至少需要选择一种字符类型")

    if exclude_confusing:
        filtered_sets = []
        for char_set in char_sets:
            filtered = ''.join(c for c in char_set if c not in CONFUSING_CHARS)
            if filtered:
                filtered_sets.append(filtered)
        char_sets = filtered_sets
        if not char_sets:
            raise ValueError("排除易混淆字符后无可用字符")

    all_chars = ''.join(char_sets)

    password = []
    for char_set in char_sets:
        if char_set:
            password.append(random.choice(char_set))

    remaining = length - len(password)
    if remaining > 0:
        password.extend(random.choices(all_chars, k=remaining))

    random.shuffle(password)
    return ''.join(password)


def generate_multiple_passwords(count: int = 1, **kwargs) -> list:
    """批量生成随机密码

    Args:
        count: 生成数量，默认为1，范围1-100
        **kwargs: 传递给generate_single_password的参数

    Returns:
        生成的密码列表

    Raises:
        ValueError: 当生成数量不在1-100范围内时抛出
    """
    if count < 1 or count > 100:
        raise ValueError("生成数量必须在1-100之间")

    return [generate_single_password(**kwargs) for _ in range(count)]
