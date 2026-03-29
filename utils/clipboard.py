from typing import Optional


class ClipboardManager:
    """剪贴板管理类"""
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        将文本复制到剪贴板
        
        Args:
            text: 要复制的文本内容
            
        Returns:
            复制是否成功
        """
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            print("⚠️ 未安装pyperclip库，请运行: pip install pyperclip")
            return False
        except Exception as e:
            print(f"⚠️ 复制到剪贴板失败: {e}")
            return False
    
    @staticmethod
    def get_from_clipboard() -> Optional[str]:
        """
        从剪贴板获取文本
        
        Returns:
            剪贴板中的文本内容，失败返回None
        """
        try:
            import pyperclip
            return pyperclip.paste()
        except ImportError:
            print("⚠️ 未安装pyperclip库，请运行: pip install pyperclip")
            return None
        except Exception as e:
            print(f"⚠️ 从剪贴板获取失败: {e}")
            return None
