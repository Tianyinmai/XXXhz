from core.password_generator import generate_single_password, generate_multiple_passwords
from utils.strength_checker import check_password_strength
from utils.clipboard import copy_to_clipboard
from utils.history import save_to_history


def show_menu() -> None:
    """显示主菜单"""
    print("\n===== 随机密码生成器 =====")
    print("1. 生成单个密码")
    print("2. 批量生成密码")
    print("3. 查看历史记录")
    print("4. 关于")
    print("0. 退出")


def get_valid_integer(prompt: str, min_val: int, max_val: int, default: int = None) -> int:
    """获取有效的整数输入

    Args:
        prompt: 提示信息
        min_val: 最小值
        max_val: 最大值
        default: 默认值

    Returns:
        有效的整数
    """
    while True:
        try:
            user_input = input(prompt)
            if not user_input and default is not None:
                return default
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"输入无效，请输入{min_val}-{max_val}之间的数字")
        except ValueError:
            if default is not None:
                print(f"输入无效，请输入数字（默认为{default}）")
            else:
                print("输入无效，请输入数字")


def get_char_types() -> tuple:
    """获取字符类型选择

    Returns:
        (use_digits, use_lower, use_upper, use_special)
    """
    print("\n选择字符类型（多选，空格分隔，默认全选）：")
    print("1. 数字  2. 小写字母  3. 大写字母  4. 特殊符号")
    print("示例：输入 '1 2 3' 表示选择数字、小写和大写字母")

    while True:
        user_input = input("请输入选项：").strip()
        if not user_input:
            return True, True, True, True

        try:
            selections = set(int(x) for x in user_input.split())
            if all(1 <= s <= 4 for s in selections):
                return (
                    1 in selections,
                    2 in selections,
                    3 in selections,
                    4 in selections
                )
            print("输入无效，请输入1-4之间的数字")
        except ValueError:
            print("输入无效，请输入正确的格式")


def get_exclude_confusing() -> bool:
    """获取是否排除易混淆字符

    Returns:
        是否排除
    """
    while True:
        user_input = input("\n是否排除易混淆字符(0/O/1/l/I)？(y/n，默认n)：").strip().lower()
        if not user_input or user_input == 'n':
            return False
        if user_input == 'y':
            return True
        print("输入无效，请输入y或n")


def generate_single() -> None:
    """生成单个密码流程"""
    length = get_valid_integer("\n请输入密码长度(6-32，默认16)：", 6, 32, 16)
    use_digits, use_lower, use_upper, use_special = get_char_types()
    exclude_confusing = get_exclude_confusing()

    try:
        password = generate_single_password(
            length=length,
            use_digits=use_digits,
            use_lower=use_lower,
            use_upper=use_upper,
            use_special=use_special,
            exclude_confusing=exclude_confusing
        )
        strength = check_password_strength(password)

        print(f"\n生成的密码：{password}")
        print(f"密码强度：{strength}")

        save_to_history([password], [strength])
        print("密码已自动保存到passwords.json")

        copy_to_clipboard(password)
        print("密码已复制到剪贴板" if copy_to_clipboard(password) else "")

    except ValueError as e:
        print(f"错误：{e}")


def generate_batch() -> None:
    """批量生成密码流程"""
    count = get_valid_integer("\n请输入生成数量(1-100，默认1)：", 1, 100, 1)
    length = get_valid_integer("请输入密码长度(6-32，默认16)：", 6, 32, 16)
    use_digits, use_lower, use_upper, use_special = get_char_types()
    exclude_confusing = get_exclude_confusing()

    try:
        passwords = generate_multiple_passwords(
            count=count,
            length=length,
            use_digits=use_digits,
            use_lower=use_lower,
            use_upper=use_upper,
            use_special=use_special,
            exclude_confusing=exclude_confusing
        )
        strengths = [check_password_strength(p) for p in passwords]

        print("\n生成的密码列表：")
        for i, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
            print(f"{i}. {pwd} [强度：{strength}]")

        save_to_history(passwords, strengths)
        print(f"\n共生成{count}个密码，已保存到passwords.json")

    except ValueError as e:
        print(f"错误：{e}")


def show_history() -> None:
    """显示历史记录"""
    from utils.history import load_history
    history = load_history()

    if not history:
        print("\n暂无历史记录")
        return

    print("\n===== 历史记录 =====")
    for i, record in enumerate(reversed(history[-5:]), 1):
        print(f"\n[{len(history) - i + 1}] 生成时间：{record.get('生成时间', '未知')}")
        passwords = record.get('密码列表', [])
        strengths = record.get('强度', [])
        for pwd, strength in zip(passwords, strengths):
            print(f"  - {pwd} [强度：{strength}]")


def show_about() -> None:
    """显示关于信息"""
    print("\n===== 关于 =====")
    print("随机密码生成器 v1.0")
    print("支持自定义长度、字符类型、批量生成")
    print("自动保存历史记录到passwords.json")


def run() -> None:
    """运行主程序"""
    while True:
        show_menu()
        choice = input("\n请选择操作：").strip()

        if choice == '1':
            generate_single()
        elif choice == '2':
            generate_batch()
        elif choice == '3':
            show_history()
        elif choice == '4':
            show_about()
        elif choice == '0':
            print("感谢使用，再见！")
            break
        else:
            print("输入无效，请选择正确的选项")
