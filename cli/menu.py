import json
import os
from datetime import datetime
from typing import List, Optional

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.password_generator import PasswordGenerator
from utils.strength_checker import StrengthChecker
from utils.clipboard import ClipboardManager


class PasswordMenu:
    """密码生成器交互菜单类"""
    
    PASSWORDS_FILE = "passwords.json"
    
    def __init__(self):
        self.generator = PasswordGenerator()
        self.strength_checker = StrengthChecker()
        self.clipboard = ClipboardManager()
    
    def clear_screen(self):
        """清空屏幕"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """打印程序标题"""
        print("\n" + "=" * 30)
        print("    随机密码生成器")
        print("=" * 30)
    
    def print_menu(self):
        """打印主菜单"""
        self.print_header()
        print("\n1. 生成单个密码")
        print("2. 批量生成密码")
        print("3. 查看历史生成记录")
        print("4. 清空历史记录")
        print("0. 退出程序")
        print("-" * 30)
    
    def get_length_input(self) -> int:
        """
        获取密码长度输入
        
        Returns:
            密码长度
        """
        while True:
            try:
                user_input = input("请设置密码长度（6-32，默认16）：").strip()
                if not user_input:
                    return 16
                length = int(user_input)
                if 6 <= length <= 32:
                    return length
                print("⚠️ 密码长度必须在6-32位之间，请重新输入")
            except ValueError:
                print("⚠️ 请输入有效的数字")
    
    def get_char_types_input(self) -> List[int]:
        """
        获取字符类型选择
        
        Returns:
            字符类型列表
        """
        while True:
            try:
                user_input = input("请选择字符类型（可多选，用逗号分隔：1.数字 2.小写字母 3.大写字母 4.特殊符号）：").strip()
                if not user_input:
                    return [1, 2, 3, 4]
                
                char_types = []
                for item in user_input.split(','):
                    char_type = int(item.strip())
                    if char_type not in [1, 2, 3, 4]:
                        print(f"⚠️ 无效的字符类型: {char_type}")
                        continue
                    if char_type not in char_types:
                        char_types.append(char_type)
                
                if char_types:
                    return char_types
                print("⚠️ 至少需要选择一种字符类型")
            except ValueError:
                print("⚠️ 请输入有效的数字，用逗号分隔")
    
    def get_exclude_confusing_input(self) -> bool:
        """
        获取是否排除易混淆字符的选择
        
        Returns:
            是否排除易混淆字符
        """
        while True:
            user_input = input("是否排除易混淆字符（y/n，默认n）：").strip().lower()
            if not user_input:
                return False
            if user_input in ['y', 'yes', '是']:
                return True
            if user_input in ['n', 'no', '否']:
                return False
            print("⚠️ 请输入 y 或 n")
    
    def get_copy_input(self) -> bool:
        """
        获取是否复制到剪贴板的选择
        
        Returns:
            是否复制到剪贴板
        """
        while True:
            user_input = input("是否复制到剪贴板（y/n）：").strip().lower()
            if user_input in ['y', 'yes', '是']:
                return True
            if user_input in ['n', 'no', '否', '']:
                return False
            print("⚠️ 请输入 y 或 n")
    
    def get_count_input(self) -> int:
        """
        获取批量生成数量
        
        Returns:
            生成数量
        """
        while True:
            try:
                user_input = input("请输入生成数量（1-100，默认1）：").strip()
                if not user_input:
                    return 1
                count = int(user_input)
                if 1 <= count <= 100:
                    return count
                print("⚠️ 生成数量必须在1-100之间，请重新输入")
            except ValueError:
                print("⚠️ 请输入有效的数字")
    
    def save_passwords(self, passwords: List[str], strengths: List[str]):
        """
        保存密码到JSON文件
        
        Args:
            passwords: 密码列表
            strengths: 强度列表
        """
        data = {
            "生成时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "密码列表": passwords,
            "强度": strengths
        }
        
        history = []
        if os.path.exists(self.PASSWORDS_FILE):
            try:
                with open(self.PASSWORDS_FILE, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    if not isinstance(history, list):
                        history = []
            except (json.JSONDecodeError, IOError):
                history = []
        
        history.append(data)
        
        try:
            with open(self.PASSWORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 密码已保存到 {self.PASSWORDS_FILE}")
        except IOError as e:
            print(f"⚠️ 保存文件失败: {e}")
    
    def view_history(self):
        """查看历史生成记录"""
        self.print_header()
        print("\n📜 历史生成记录")
        print("-" * 50)
        
        if not os.path.exists(self.PASSWORDS_FILE):
            print("暂无历史记录")
            return
        
        try:
            with open(self.PASSWORDS_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            if not history:
                print("暂无历史记录")
                return
            
            for i, record in enumerate(history, 1):
                print(f"\n记录 #{i}")
                print(f"生成时间: {record.get('生成时间', '未知')}")
                passwords = record.get('密码列表', [])
                strengths = record.get('强度', [])
                
                for j, (pwd, strength) in enumerate(zip(passwords, strengths), 1):
                    print(f"  密码{j}: {pwd} [{strength}]")
            
            print("-" * 50)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ 读取历史记录失败: {e}")
    
    def clear_history(self):
        """清空历史记录"""
        if not os.path.exists(self.PASSWORDS_FILE):
            print("\n⚠️ 暂无历史记录")
            return
        
        confirm = input("确认清空所有历史记录？（y/n）：").strip().lower()
        if confirm in ['y', 'yes', '是']:
            try:
                os.remove(self.PASSWORDS_FILE)
                print("✅ 历史记录已清空")
            except IOError as e:
                print(f"⚠️ 清空失败: {e}")
        else:
            print("已取消操作")
    
    def generate_single(self):
        """生成单个密码"""
        self.print_header()
        print("\n📝 生成单个密码")
        print("-" * 30)
        
        length = self.get_length_input()
        char_types = self.get_char_types_input()
        exclude_confusing = self.get_exclude_confusing_input()
        
        try:
            password = self.generator.generate_password(
                length=length,
                char_types=char_types,
                exclude_confusing=exclude_confusing
            )
            strength, score = self.strength_checker.check(password)
            
            print(f"\n生成的密码：{password}")
            print(f"密码强度：{strength}（分数：{score}）")
            
            if self.get_copy_input():
                if self.clipboard.copy_to_clipboard(password):
                    print("✅ 密码已复制到剪贴板！")
            
            self.save_passwords([password], [strength])
            
        except ValueError as e:
            print(f"⚠️ 错误: {e}")
    
    def generate_batch(self):
        """批量生成密码"""
        self.print_header()
        print("\n📝 批量生成密码")
        print("-" * 30)
        
        count = self.get_count_input()
        length = self.get_length_input()
        char_types = self.get_char_types_input()
        exclude_confusing = self.get_exclude_confusing_input()
        
        try:
            passwords = self.generator.generate_batch(
                count=count,
                length=length,
                char_types=char_types,
                exclude_confusing=exclude_confusing
            )
            
            strengths = []
            print(f"\n生成的密码：")
            print("-" * 50)
            for i, password in enumerate(passwords, 1):
                strength, score = self.strength_checker.check(password)
                strengths.append(strength)
                print(f"{i:3d}. {password} [{strength}]")
            print("-" * 50)
            
            if count == 1:
                if self.get_copy_input():
                    if self.clipboard.copy_to_clipboard(passwords[0]):
                        print("✅ 密码已复制到剪贴板！")
            else:
                copy_all = input("是否复制所有密码到剪贴板？（y/n）：").strip().lower()
                if copy_all in ['y', 'yes', '是']:
                    if self.clipboard.copy_to_clipboard('\n'.join(passwords)):
                        print("✅ 所有密码已复制到剪贴板！")
            
            self.save_passwords(passwords, strengths)
            
        except ValueError as e:
            print(f"⚠️ 错误: {e}")
    
    def run(self):
        """运行主菜单"""
        while True:
            self.print_menu()
            choice = input("请选择功能（0-4）：").strip()
            
            if choice == '1':
                self.generate_single()
                input("\n按回车键继续...")
            elif choice == '2':
                self.generate_batch()
                input("\n按回车键继续...")
            elif choice == '3':
                self.view_history()
                input("\n按回车键继续...")
            elif choice == '4':
                self.clear_history()
                input("\n按回车键继续...")
            elif choice == '0':
                print("\n👋 感谢使用，再见！")
                break
            else:
                print("⚠️ 无效的选择，请重新输入")
                input("\n按回车键继续...")
