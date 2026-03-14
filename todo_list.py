def add_todo(todo_list, content):
    todo = {"content": content, "done": False}
    todo_list.append(todo)
    print(f"待办事项添加成功：{content}")

def mark_todo_done(todo_list, index):
    if 0 <= index < len(todo_list):
        todo_list[index]["done"] = True
        print(f"已标记完成：{todo_list[index]['content']}")
    else:
        print("无效的待办序号")

def delete_todo(todo_list, index):
    if 0 <= index < len(todo_list):
        deleted = todo_list.pop(index)
        print(f"已删除：{deleted['content']}")
    else:
        print("无效的待办序号")

def show_all_todos(todo_list):
    if not todo_list:
        print("暂无待办事项")
        return False
    print("\n===== 待办事项列表 =====")
    for i, todo in enumerate(todo_list):
        status = "已完成" if todo["done"] else "未完成"
        print(f"{i+1}. [{status}] {todo['content']}")
    return True

def main():
    todo_list = []
    while True:
        print("\n请选择操作：1-添加待办 2-查看待办 3-标记完成 4-删除待办 5-退出")
        choice = input("请输入选项: ").strip()
        if choice == '1':
            while True:
                content = input("请输入待办内容: ").strip()
                if content:
                    add_todo(todo_list, content)
                    break
                else:
                    print("待办内容不能为空，请重新输入")
        elif choice == '2':
            show_all_todos(todo_list)
        elif choice == '3':
            if show_all_todos(todo_list):
                while True:
                    try:
                        index = int(input("请输入要标记完成的待办序号: ")) - 1
                        if 0 <= index < len(todo_list):
                            mark_todo_done(todo_list, index)
                            break
                        else:
                            print("输入错误，请重新输入")
                    except ValueError:
                        print("输入错误，请重新输入")
        elif choice == '4':
            if show_all_todos(todo_list):
                while True:
                    try:
                        index = int(input("请输入要删除的待办序号: ")) - 1
                        if 0 <= index < len(todo_list):
                            delete_todo(todo_list, index)
                            break
                        else:
                            print("输入错误，请重新输入")
                    except ValueError:
                        print("输入错误，请重新输入")
        elif choice == '5':
            print("感谢使用待办事项管理工具！")
            break
        else:
            print("输入错误，请重新输入")

if __name__ == "__main__":
    main()
