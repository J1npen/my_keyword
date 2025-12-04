import my_keyword

def menu3_2():
    print('''
===================
1. 查询所有 keyword
2. 查询所有网站
3. 按网站名称查询
4. 按喜爱程度查询
5. 按备注模糊查询
6. 支持模糊查询
===================          
''')

def menu1_2():
    print('''
===================
1. 单个添加
2. 根据网站批量添加
===================          
''')

def menu():
    print('''
===================
1. 添加 keyword
2. 修改 keyword
3. 查询 keyword
4. 退出
输入 exit 退出程序
===================          
''')

def menu_level_1():
    menu1_2()

    menu_actions = {
        '1': my_keyword.add_keyword,
        '2': lambda: print('功能暂未开发！请耐心等待...')
    }

    choice = input('选择你需要的功能选项：').strip()

    action = menu_actions.get(choice)
    if action:
            action()
    else:
        print('输入无效，退回主菜单！')
    

def menu_level_2():
    pass

def menu_level_3():
    menu3_2()
    choice = input('选择你需要的功能选项：').strip()

    actions = {
        '1': my_keyword.query_keyword,
        '2': my_keyword.query_site,
        '3': my_keyword.query_by_site,
        '4': my_keyword.query_by_rating,
        '5': lambda: print("功能 5 执行"),
        '6': lambda: print("功能 6 执行"),
    }

    action = actions.get(choice)
    if action:
        action()
    else:
        print("输入无效！")

def exit_program():
    print('程序退出！再见！')
    exit()

def main():
    gap_time = 0
    loop = 0

    # ------- First-level menu mapping function -------
    menu_actions = {
        '1': menu_level_1,
        '2': menu_level_2,
        '3': menu_level_3,
        '4': exit_program,
        'exit': exit_program,
    }

    menu()
    choice = input('选择你需要的功能选项：').strip()
    while True:
        loop += 1

        if not loop == 1:
            if choice: print('回车以查看主菜单') # If the menu has already appeared, there's no need to print the output.
            choice = input().strip()

        if not choice:
            gap_time += 1
            if gap_time >= 3:
                print('长时间未操作，程序退出！')
                break
            menu()
            continue

        gap_time = 0 # Reset gap_time value

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print('输入无效，请重新输入！')
            gap_time += 1
        


if __name__ == '__main__':
    main()