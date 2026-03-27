def copy_to_clipboard(text: str) -> bool:
    """复制文本到剪贴板

    Args:
        text: 要复制的文本

    Returns:
        复制成功返回True，失败返回False
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        print("提示：未安装pyperclip库，无法使用剪贴板功能")
        print("如需安装，请执行：pip install pyperclip")
        return False
    except Exception as e:
        print(f"剪贴板操作失败：{e}")
        return False
