import os
import sys
import time
import tkinter
import tkinter.messagebox

import win32api
import win32con
import win32gui


# 获取桌面分辨率
def get_screen_resolution():
    x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    return f"{x}*{y}"


# 模拟记住我,以便下次不需要重新填写安装地址
def save_msg(qq_entry, pl_sql_entry, chrome_entry):
    save_dict = {
        'qq': qq_entry.get(),
        'pl/sql': pl_sql_entry.get(),
        'chrome': chrome_entry.get()
    }
    print(save_dict)
    with open(r'E:\app_open_info.txt', "w") as f:  # 传入标识符'w'或者'wb'表示写文本文件或写二进制文件
        f.write(str(save_dict))


# 获取本地保存信息,填充到输入框
def read_msg(qq_str, pl_sql_str, chrome_str):
    flag = os.path.exists(r'E:\app_open_info.txt')
    if flag:
        with open(r'E:\app_open_info.txt', "r") as f:  # 传入标识符'r'表示读取文件
            msg_str = f.read()
        msg_dict = eval(msg_str)
        print(f"read:{msg_dict}")
        qq_str.set(msg_dict['qq'])
        pl_sql_str.set(msg_dict['pl/sql'])
        chrome_str.set(msg_dict['chrome'])
    else:
        pass


# 关闭窗口
def quit_tk(root):
    root.quit()


# 打开应用并且鼠标点击按钮（获取按钮的像素坐标很麻烦）
def open_by_grab():
    # 隐藏cmd
    # ct = win32api.GetConsoleTitle()
    # hd = win32gui.FindWindow(0, ct)
    # win32gui.ShowWindow(hd, 0)
    # 打开应用
    for key in appdict.keys():
        print(f"启动 {key} ...")
        if appdict[key] == '':
            print(f"不处理{key} ...")
            pass
        else:
            if key in excludeTup:
                os.popen(r'%s' % appdict[key])  # os.system会阻塞
                print(f"获取{key}成功,打开 ...")
                pass
            else:
                os.popen(r'%s' % appdict[key])  # os.system会阻塞
                time.sleep(3)
                winhd = win32gui.FindWindow(None, namedict[key])
                while winhd == 0:
                    print("等待获取%s窗口 ..." % key)
                    time.sleep(3)
                    winhd = win32gui.FindWindow(None, namedict[key])
                print("获取%s窗口成功,开始登录 ..." % key)
                a, b = coorddict[key]
                mouse_click(a, b)
                time.sleep(3)
    print("完毕 ...")
    time.sleep(1)


# 模拟鼠标点击
def mouse_click(a, b):
    time.sleep(1)
    win32api.SetCursorPos((a, b))
    time.sleep(1)
    # win32api.keybd_event(13, 0, 0, 0)   # 模拟键盘输入enter
    # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放按键
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 360拦截了虚拟按键,可以添加信任或者关闭360
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 自动打开
def auto_open(root, qq_entry, pl_sql_entry, chrome_entry):
    appdict['qq'] = qq_entry.get()
    appdict['pl/sql'] = pl_sql_entry.get()
    appdict['chrome'] = chrome_entry.get()
    if appdict['qq'] != '' and not appdict['qq'].endswith('exe'):
        tkinter.messagebox.showinfo('提示', '不是正确的qq安装地址')
    elif appdict['pl/sql'] != '' and not appdict['pl/sql'].endswith('exe'):
        tkinter.messagebox.showinfo('提示', '不是正确的pl/sql安装地址')
    elif appdict['chrome'] != '' and not appdict['chrome'].endswith('exe'):
        tkinter.messagebox.showinfo('提示', '不是正确的chrome安装地址')
    else:
        open_by_grab()
        quit_tk(root)


# 界面
def draw_interface():
    root = tkinter.Tk()     # 创建顶层窗口
    root.geometry('800x500')     # 初始化窗口大小
    root.title("自动打开app")   # 标题
    # 设置错误信息标签
    error_str = tkinter.StringVar()
    error_label = tkinter.Label(root, textvariable=error_str, anchor='w', disabledforeground='white',
                                activeforeground='black', activebackground='red', state='disable')
    error_label.place(x=100, y=20, height=20)
    # 设置简介标签
    screen_resolution = get_screen_resolution()
    introduce_str = tkinter.StringVar()
    introduce_str.set(f"说明：目前仅适用于1920*1080的屏幕,程序获取到的分辨率为：{screen_resolution}")
    introduce_label = tkinter.Label(root, textvariable=introduce_str, anchor='w', width=120)
    introduce_label.place(x=100, y=50, height=20)

    if screen_resolution == '1920*1080':
        # qq
        qq_str = tkinter.StringVar()
        qq_label = tkinter.Label(root, text='QQ安装地址:', anchor='w')
        qq_label.place(x=100, y=80, width=120, height=20)
        qq_entry = tkinter.Entry(root, bd=1, textvariable=qq_str)
        qq_entry.place(x=230, y=80, width=470, height=20)
        qq_example_label = tkinter.Label(root, text='举例:D:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe',
                                         foreground='gray', anchor='w')
        qq_example_label.place(x=100, y=105, height=20)
        # pl/sql
        pl_sql_str = tkinter.StringVar(value='')
        pl_sql_label = tkinter.Label(root, text='pl/sql安装地址:', anchor='w')
        pl_sql_label.place(x=100, y=140, width=120, height=20)
        pl_sql_entry = tkinter.Entry(root, bd=1, textvariable=pl_sql_str)
        pl_sql_entry.place(x=230, y=140, width=470, height=20)
        pl_sql_example_label = tkinter.Label(root, text='举例:E:\PLSQL Developer\plsqldev.exe',
                                             foreground='gray', anchor='w')
        pl_sql_example_label.place(x=100, y=165, height=20)
        # chrome
        chrome_str = tkinter.StringVar(value='')
        chrome_label = tkinter.Label(root, text='chrome安装地址:', anchor='w')
        chrome_label.place(x=100, y=200, width=120, height=20)
        chrome_entry = tkinter.Entry(root, bd=1, textvariable=chrome_str)
        chrome_entry.place(x=230, y=200, width=470, height=20)
        chrome_example_label = tkinter.Label(root,
                                             text='举例:C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                                             foreground='gray', anchor='w')
        chrome_example_label.place(x=100, y=225, height=20)
        # 获取本地保存信息,填充到输入框
        read_msg(qq_str, pl_sql_str, chrome_str)
        # 保存信息到本地
        button_save = tkinter.Button(root, text='记住我', command=lambda: save_msg(qq_entry, pl_sql_entry, chrome_entry))
        button_save.place(x=100, y=260, width=50, height=30)
        save_introduce__label = tkinter.Label(root, text='模拟记住我,以便下次不需要重新填写安装地址', foreground='gray',
                                              anchor='center')
        save_introduce__label.place(x=170, y=260, height=30)
        # 自动打开
        # noinspection PyBroadException
        try:
            button_save = tkinter.Button(root, text='自动启动', command=lambda: auto_open(root, qq_entry, pl_sql_entry,
                                                                                       chrome_entry))
            button_save.place(x=100, y=300, width=80, height=30)
        except Exception:
            error_str.set("启动出现异常...")
            error_label.config(state='active')
    else:
        error_str.set("分辨率不符合...")
        error_label.config(state='active')
    root.mainloop()


'''
自动登录程序,可扩展
'''
if __name__ == '__main__':
    appdict = {'qq': '',
               'pl/sql': '',
               'chrome': ''}
    coorddict = {'qq': [960, 665], 'pl/sql': [1060, 620], 'idea': [700, 245]}
    namedict = {'qq': 'QQ', 'pl/sql': 'Oracle Logon', 'idea': 'Welcome to IntelliJ IDEA'}
    excludeTup = ('chrome', 'notepad')
    exename = str(sys.executable)
    draw_interface()
    # 打包成py.exe后运行发现由于os.popen的原因,导致cmd.exe始终不会自动关闭,所以做以下操作
    exehd = win32gui.FindWindow(None, exename)
    if exehd != 0:
        win32gui.SendMessage(exehd, win32con.WM_CLOSE)
    else:
        print("找不到openapp2.exe")
