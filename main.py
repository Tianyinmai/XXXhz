import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.menu import PasswordMenu


def main():
    """程序主入口"""
    try:
        menu = PasswordMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
    except Exception as e:
        print(f"\n⚠️ 程序发生错误: {e}")


if __name__ == "__main__":
    main()
