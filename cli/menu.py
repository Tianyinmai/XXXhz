import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.password_generator import generate_single_password, generate_batch_passwords
from utils.strength_checker import check_password_strength
from utils.clipboard import copy_to_clipboard
from utils.history import save_passwords_history


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\n按回车键继续...")


def get_length_input() -> int:
    while True:
        try:
            user_input = input("请设置密码长度（6-32，默认16）：").strip()
            if not user_input:
                return 16
            length = int(user_input)
            if 6 <= length <= 32:
                return length
            else:
                print("❌ 错误：密码长度必须在6-32之间")
        except ValueError:
            print("❌ 错误：请输入有效的数字")


def get_char_types() -> tuple:
    while True:
        user_input = input("请选择字符类型（可多选，用逗号分隔：1.数字 2.小写字母 3.大写字母 4.特殊符号）：").strip()
        
        if not user_input:
            return (True, True, True, True)
        
        try:
            choices = [int(x.strip()) for x in user_input.split(',')]
            use_digits = 1 in choices
            use_lower = 2 in choices
            use_upper = 3 in choices
            use_special = 4 in choices
            
            if not any([use_digits, use_lower, use_upper, use_special]):
                print("❌ 错误：至少需要选择一种字符类型")
                continue
            
            return (use_digits, use_lower, use_upper, use_special)
        except ValueError:
            print("❌ 错误：请输入有效的选项，如：1,2,3")


def get_exclude_confusing() -> bool:
    while True:
        user_input = input("是否排除易混淆字符（y/n，默认n）：").strip().lower()
        if not user_input:
            return False
        if user_input in ['y', 'n']:
            return user_input == 'y'
        print("❌ 错误：请输入y或n")


def get_count_input() -> int:
    while True:
        try:
            user_input = input("请输入生成数量（1-100，默认1）：").strip()
            if not user_input:
                return 1
            count = int(user_input)
            if 1 <= count <= 100:
                return count
            else:
                print("❌ 错误：生成数量必须在1-100之间")
        except ValueError:
            print("❌ 错误：请输入有效的数字")


def single_password_menu():
    clear_screen()
    print("===== 生成单个密码 =====")
    
    length = get_length_input()
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
        save_passwords_history([password], [strength])
        
        print(f"\n生成的密码：{password}")
        print(f"密码强度：{strength}")
        
        while True:
            copy_choice = input("\n是否复制到剪贴板（y/n）：").strip().lower()
            if copy_choice == 'y':
                if copy_to_clipboard(password):
                    print("✅ 密码已复制到剪贴板！")
                break
            elif copy_choice == 'n':
                break
            else:
                print("❌ 错误：请输入y或n")
        
    except ValueError as e:
        print(f"\n❌ 生成失败：{str(e)}")
    
    pause()


def batch_password_menu():
    clear_screen()
    print("===== 批量生成密码 =====")
    
    count = get_count_input()
    length = get_length_input()
    use_digits, use_lower, use_upper, use_special = get_char_types()
    exclude_confusing = get_exclude_confusing()
    
    try:
        passwords = generate_batch_passwords(
            count=count,
            length=length,
            use_digits=use_digits,
            use_lower=use_lower,
            use_upper=use_upper,
            use_special=use_special,
            exclude_confusing=exclude_confusing
        )
        
        strengths = [check_password_strength(pwd) for pwd in passwords]
        save_passwords_history(passwords, strengths)
        
        print(f"\n✅ 成功生成{len(passwords)}个密码：\n")
        for i, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
            print(f"{i:2d}. {pwd} [{strength}]")
        
    except ValueError as e:
        print(f"\n❌ 生成失败：{str(e)}")
    
    pause()


def show_history_menu():
    clear_screen()
    print("===== 历史生成记录 =====")
    
    from utils.history import load_history
    history = load_history()
    
    if not history:
        print("\n暂无历史记录")
    else:
        for i, record in enumerate(reversed(history), 1):
            print(f"\n--- 记录 {i} ---")
            print(f"生成时间：{record.get('生成时间', '未知')}")
            for j, (pwd, strength) in enumerate(zip(record.get('密码列表', []), record.get('强度', [])), 1):
                print(f"{j}. {pwd} [{strength}]")
    
    pause()


def clear_history_menu():
    clear_screen()
    print("===== 清空历史记录 =====")
    
    while True:
        confirm = input("\n确认清空所有历史记录？(y/n)：").strip().lower()
        if confirm == 'y':
            from utils.history import clear_history
            if clear_history():
                print("\n✅ 历史记录已清空")
            else:
                print("\n❌ 清空失败")
            break
        elif confirm == 'n':
            print("\n已取消操作")
            break
        print("❌ 错误：请输入y或n")
    
    pause()


def show_main_menu():
    clear_screen()
    print("===== 随机密码生成器 =====")
    print("1. 生成单个密码")
    print("2. 批量生成密码")
    print("3. 查看历史生成记录")
    print("4. 清空历史记录")
    print("0. 退出程序")
    print()


def get_menu_choice() -> str:
    while True:
        choice = input("请选择功能（0-4）：").strip()
        if choice in ['0', '1', '2', '3', '4']:
            return choice
        print("❌ 错误：请输入0-4之间的数字")


def main():
    while True:
        show_main_menu()
        choice = get_menu_choice()
        
        if choice == '1':
            single_password_menu()
        elif choice == '2':
            batch_password_menu()
        elif choice == '3':
            show_history_menu()
        elif choice == '4':
            clear_history_menu()
        elif choice == '0':
            print("\n感谢使用随机密码生成器！")
            break
