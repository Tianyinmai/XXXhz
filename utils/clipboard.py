"""
剪贴板操作模块
提供复制文本到剪贴板的功能
"""

from typing import Optional


class ClipboardManager:
    """剪贴板管理器类"""
    
    def __init__(self):
        """初始化剪贴板管理器"""
        self._pyperclip_available = self._check_pyperclip()
    
    def _check_pyperclip(self) -> bool:
        """
        检查 pyperclip 库是否可用
        
        Returns:
            是否可用
        """
        try:
            import pyperclip
            return True
        except ImportError:
            return False
    
    def copy(self, text: str) -> bool:
        """
        复制文本到剪贴板
        
        Args:
            text: 要复制的文本
            
        Returns:
            是否复制成功
        """
        if not self._pyperclip_available:
            return False
        
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except Exception:
            return False
    
    def copy_batch(self, texts: list, separator: str = "\n") -> bool:
        """
        批量复制文本到剪贴板
        
        Args:
            texts: 要复制的文本列表
            separator: 分隔符
            
        Returns:
            是否复制成功
        """
        combined_text = separator.join(texts)
        return self.copy(combined_text)
    
    def is_available(self) -> bool:
        """
        检查剪贴板功能是否可用
        
        Returns:
            是否可用
        """
        return self._pyperclip_available
    
    def get_install_hint(self) -> str:
        """
        获取安装 pyperclip 的提示信息
        
        Returns:
            安装提示字符串
        """
        return "提示：剪贴板功能需要 pyperclip 库，请运行 'pip install pyperclip' 安装"


# 便捷函数
def copy_to_clipboard(text: str) -> bool:
    """
    复制文本到剪贴板的便捷函数
    
    Args:
        text: 要复制的文本
        
    Returns:
        是否复制成功
    """
    manager = ClipboardManager()
    return manager.copy(text)
