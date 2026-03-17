"""
随机密码生成器 - 主程序入口

功能：
- 生成单个/批量随机密码
- 密码强度检测
- 历史记录管理
- 剪贴板复制

使用方法：
    python main.py
"""

import sys
import os

# 添加当前目录到路径，确保可以导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.password_generator import PasswordGenerator
from utils.strength_checker import StrengthChecker
from utils.clipboard import ClipboardManager
from cli.menu import Menu


class PasswordGeneratorApp:
    """密码生成器应用程序类"""
    
    def __init__(self):
        """初始化应用程序"""
        self.generator = PasswordGenerator()
        self.checker = StrengthChecker()
        self.clipboard = ClipboardManager()
        self.menu = Menu()
    
    def _char_types_to_bools(self, char_types: list) -> dict:
        """
        将字符类型列表转换为布尔值字典
        
        Args:
            char_types: 字符类型列表（1-4）
            
        Returns:
            布尔值字典
        """
        return {
            'use_digits': 1 in char_types,
            'use_lowercase': 2 in char_types,
            'use_uppercase': 3 in char_types,
            'use_special': 4 in char_types
        }
    
    def generate_single_password(self) -> None:
        """生成单个密码"""
        try:
            # 获取配置
            length, char_types, exclude_confusing = self.menu.get_password_config()
            bools = self._char_types_to_bools(char_types)
            
            # 生成密码
            password = self.generator.generate(
                length=length,
                use_digits=bools['use_digits'],
                use_lowercase=bools['use_lowercase'],
                use_uppercase=bools['use_uppercase'],
                use_special=bools['use_special'],
                exclude_confusing=exclude_confusing
            )
            
            # 检测强度
            strength = self.checker.check(password)
            
            # 显示结果
            self.menu.display_password(password, strength)
            
            # 保存到历史
            self.generator.save_to_history([password], [strength])
            
            # 询问是否复制
            if self.menu.ask_copy_to_clipboard():
                success = self.clipboard.copy(password)
                self.menu.show_clipboard_status(success)
            
        except ValueError as e:
            self.menu.show_message(str(e), is_error=True)
    
    def generate_batch_passwords(self) -> None:
        """批量生成密码"""
        try:
            # 获取配置
            length, char_types, exclude_confusing = self.menu.get_password_config()
            count = self.menu.get_batch_count()
            bools = self._char_types_to_bools(char_types)
            
            # 生成密码
            passwords = self.generator.generate_batch(
                count=count,
                length=length,
                use_digits=bools['use_digits'],
                use_lowercase=bools['use_lowercase'],
                use_uppercase=bools['use_uppercase'],
                use_special=bools['use_special'],
                exclude_confusing=exclude_confusing
            )
            
            # 检测强度
            strengths = self.checker.check_batch(passwords)
            
            # 显示结果
            self.menu.display_passwords_batch(passwords, strengths)
            
            # 保存到历史
            self.generator.save_to_history(passwords, strengths)
            
            # 询问是否复制
            if self.menu.ask_copy_to_clipboard(is_batch=True):
                success = self.clipboard.copy_batch(passwords)
                self.menu.show_clipboard_status(success)
            
        except ValueError as e:
            self.menu.show_message(str(e), is_error=True)
    
    def view_history(self) -> None:
        """查看历史记录"""
        history = self.generator.get_history()
        self.menu.display_history(history)
    
    def clear_history(self) -> None:
        """清空历史记录"""
        if self.menu.confirm_clear_history():
            if self.generator.clear_history():
                self.menu.show_message("历史记录已清空")
            else:
                self.menu.show_message("清空历史记录失败", is_error=True)
    
    def run(self) -> None:
        """运行应用程序主循环"""
        # 显示剪贴板库提示（如果未安装）
        if not self.clipboard.is_available():
            print(f"\n{self.clipboard.get_install_hint()}")
        
        while True:
            choice = self.menu.show_main_menu()
            
            if choice == '0':
                self.menu.exit_program()
            
            elif choice == '1':
                self.generate_single_password()
                self.menu.pause()
            
            elif choice == '2':
                self.generate_batch_passwords()
                self.menu.pause()
            
            elif choice == '3':
                self.view_history()
                self.menu.pause()
            
            elif choice == '4':
                self.clear_history()
                self.menu.pause()


def main():
    """
    程序入口函数
    
    创建并运行密码生成器应用程序
    """
    app = PasswordGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()
