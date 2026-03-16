def copy_to_clipboard(text: str) -> bool:
    """
    复制文本到剪贴板

    Args:
        text: 需要复制的文本

    Returns:
        复制成功返回True，失败返回False
    """
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        print("⚠️  提示：pyperclip库未安装，无法使用剪贴板功能")
        print("   安装命令：pip install pyperclip")
        return False
    except Exception as e:
        print(f"⚠️  复制失败：{str(e)}")
        return False
