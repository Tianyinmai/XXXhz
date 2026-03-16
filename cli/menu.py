"""
交互菜单模块
提供命令行交互界面
"""

import sys
from typing import Optional, Tuple, List


class Menu:
    """交互菜单类"""
    
    def __init__(self):
        """初始化菜单"""
        pass
    
    def show_main_menu(self) -> str:
        """
        显示主菜单
        
        Returns:
            用户选择的选项
        """
        print("\n" + "=" * 25)
        print("     随机密码生成器")
        print("=" * 25)
        print("  1. 生成单个密码")
        print("  2. 批量生成密码")
        print("  3. 查看历史生成记录")
        print("  4. 清空历史记录")
        print("  0. 退出程序")
        print("=" * 25)
        
        while True:
            choice = input("请选择功能（0-4）：").strip()
            if choice in ['0', '1', '2', '3', '4']:
                return choice
            print("❌ 无效选择，请输入 0-4 之间的数字")
    
    def get_password_config(self) -> Tuple[int, List[int], bool]:
        """
        获取密码生成配置
        
        Returns:
            (密码长度, 字符类型列表, 是否排除易混淆字符)
        """
        # 密码长度
        while True:
            length_input = input("\n请设置密码长度（6-32，默认16）：").strip()
            if not length_input:
                length = 16
                break
            try:
                length = int(length_input)
                if 6 <= length <= 32:
                    break
                else:
                    print("❌ 密码长度必须在6-32位之间")
            except ValueError:
                print("❌ 请输入有效的数字")
        
        # 字符类型
        print("\n字符类型选项：")
        print("  1. 数字")
        print("  2. 小写字母")
        print("  3. 大写字母")
        print("  4. 特殊符号")
        
        while True:
            char_type_input = input("请选择字符类型（可多选，用逗号分隔，如 1,2,3）：").strip()
            try:
                char_types = [int(x.strip()) for x in char_type_input.split(',')]
                # 去重并验证
                char_types = list(set(char_types))
                if all(1 <= t <= 4 for t in char_types) and len(char_types) > 0:
                    break
                else:
                    print("❌ 请至少选择一种字符类型（1-4）")
            except ValueError:
                print("❌ 请输入有效的数字，用逗号分隔")
        
        # 排除易混淆字符
        while True:
            exclude_input = input("\n是否排除易混淆字符（y/n，默认n）：").strip().lower()
            if not exclude_input or exclude_input == 'n':
                exclude_confusing = False
                break
            elif exclude_input == 'y':
                exclude_confusing = True
                break
            else:
                print("❌ 请输入 y 或 n")
        
        return length, char_types, exclude_confusing
    
    def get_batch_count(self) -> int:
        """
        获取批量生成数量
        
        Returns:
            生成数量
        """
        while True:
            count_input = input("\n请输入生成数量（1-100，默认1）：").strip()
            if not count_input:
                return 1
            try:
                count = int(count_input)
                if 1 <= count <= 100:
                    return count
                else:
                    print("❌ 批量生成数量必须在1-100之间")
            except ValueError:
                print("❌ 请输入有效的数字")
    
    def display_password(self, password: str, strength: str) -> None:
        """
        显示单个密码及其强度
        
        Args:
            password: 生成的密码
            strength: 密码强度
        """
        print(f"\n生成的密码：{password}")
        print(f"密码强度：{strength}")
    
    def display_passwords_batch(self, passwords: List[str], strengths: List[str]) -> None:
        """
        批量显示密码及其强度
        
        Args:
            passwords: 密码列表
            strengths: 强度列表
        """
        print(f"\n共生成 {len(passwords)} 个密码：")
        print("-" * 40)
        for i, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
            print(f"{i:3d}. {pwd:<20} [{strength}]")
        print("-" * 40)
    
    def ask_copy_to_clipboard(self, is_batch: bool = False) -> bool:
        """
        询问是否复制到剪贴板
        
        Args:
            is_batch: 是否是批量复制
            
        Returns:
            是否复制
        """
        prompt = "\n是否复制到剪贴板（y/n）：" if not is_batch else "\n是否复制所有密码到剪贴板（y/n）："
        while True:
            choice = input(prompt).strip().lower()
            if choice == 'y':
                return True
            elif choice == 'n' or not choice:
                return False
            else:
                print("❌ 请输入 y 或 n")
    
    def display_history(self, history: List[dict]) -> None:
        """
        显示历史记录
        
        Args:
            history: 历史记录列表
        """
        if not history:
            print("\n暂无历史记录")
            return
        
        print(f"\n共 {len(history)} 条历史记录：")
        print("=" * 60)
        
        for i, record in enumerate(history, 1):
            print(f"\n【记录 {i}】")
            print(f"  生成时间：{record.get('生成时间', '未知')}")
            passwords = record.get('密码列表', [])
            strengths = record.get('强度', [])
            
            for j, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
                print(f"  密码 {j}：{pwd:<20} [{strength}]")
        
        print("\n" + "=" * 60)
    
    def confirm_clear_history(self) -> bool:
        """
        确认是否清空历史记录
        
        Returns:
            是否确认清空
        """
        while True:
            choice = input("\n确定要清空所有历史记录吗？此操作不可恢复（y/n）：").strip().lower()
            if choice == 'y':
                return True
            elif choice == 'n' or not choice:
                return False
            else:
                print("❌ 请输入 y 或 n")
    
    def show_message(self, message: str, is_error: bool = False) -> None:
        """
        显示消息
        
        Args:
            message: 消息内容
            is_error: 是否是错误消息
        """
        prefix = "❌ " if is_error else "✅ "
        print(f"\n{prefix}{message}")
    
    def show_clipboard_status(self, success: bool) -> None:
        """
        显示剪贴板操作状态
        
        Args:
            success: 是否成功
        """
        if success:
            print("\n✅ 密码已复制到剪贴板！")
        else:
            print("\n❌ 复制失败，请检查是否安装了 pyperclip 库")
            print("   运行 'pip install pyperclip' 安装")
    
    def pause(self) -> None:
        """暂停等待用户按键"""
        input("\n按回车键继续...")
    
    def exit_program(self) -> None:
        """退出程序"""
        print("\n感谢使用，再见！")
        sys.exit(0)
