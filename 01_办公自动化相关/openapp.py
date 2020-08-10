import os
import time

import win32api
import win32con
import win32gui

# 设置appdict
pyexe = "E:\python\python.exe"
appdict = {'qq': '"D:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe"',
           'pl/sql': '"E:\PLSQL Developer\plsqldev.exe"',
           'idea': '"E:\IDEA\IntelliJ IDEA Community Edition 2018.1.5\\bin\idea64.exe"',
           'chrome': '"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"',
           'notepad': '"E:\\Notepad++\\notepad++.exe"'}
coorddict = {'qq': [960, 665], 'pl/sql': [1060, 620], 'idea': [700, 245]}
namedict = {'qq': 'QQ', 'pl/sql': 'Oracle Logon', 'idea': 'Welcome to IntelliJ IDEA'}
excludeTup = ('chrome', 'notepad')

'''
# 使用spy++(E:\BaiduNetdiskDownload处)查看句柄和窗口标题
def get_all_hds():
    hdlist = []
    hddict = {}
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hdlist)
    for h in hdlist:
        wintext = win32gui.GetWindowText(h)
        if wintext == "":
            wintext = "未知"
        hddict[h] = wintext
    return hddict


def get_hd(window_name):
    winhd = win32gui.FindWindow(None, window_name)
    left, top, right, bottom = win32gui.GetWindowRect(winhd)
    wintext = win32gui.GetWindowText(winhd)
    print("句柄:%s,坐标:[%d,%d,%d,%d],窗口名:%s" % (winhd, left, top, right, bottom, wintext))
    hdchildlist = []
    # 有的界面获取不到控件句柄，比如qq
    win32gui.EnumChildWindows(winhd, lambda hwnd, param: param.append(hwnd),  hdchildlist)
    for h in hdchildlist:
        wintext = win32gui.GetWindowText(h)
        if wintext == "":
            wintext = "未知"
        print("句柄:%d,窗口名:%s" % (h, wintext))
        if wintext == "&Cancel":
            left, top, right, bottom = win32gui.GetWindowRect(h)
            print("句柄:%s,坐标:[%d,%d,%d,%d],窗口名:%s" % (h, left, top, right, bottom, wintext))
        if wintext == "QQEdit":
            left, top, right, bottom = win32gui.GetWindowRect(h)
            print("句柄:%s,坐标:[%d,%d,%d,%d],窗口名:%s" % (h, left, top, right, bottom, wintext))
'''


# 打开应用并且鼠标点击按钮（获取按钮的像素坐标很麻烦）
def open_by_grab():
    pyhd = win32gui.FindWindow(None, pyexe)
    win32gui.SetWindowPos(pyhd, win32con.HWND_TOPMOST, 0, 0, 500, 500, win32con.SWP_SHOWWINDOW)
    print("py exe 句柄: %s ..." % pyhd)
    for key in appdict.keys():
        print("启动 %s ..." % key)
        os.popen(r'%s' % appdict[key])  # os.system会阻塞
        time.sleep(3)
        if key in excludeTup:
            pass
        else:
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
    win32gui.SendMessage(pyhd, win32con.WM_CLOSE)


# 模拟鼠标点击
def mouse_click(a, b):
    time.sleep(1)
    win32api.SetCursorPos((a, b))
    time.sleep(1)
    # win32api.keybd_event(13, 0, 0, 0)   # 模拟键盘输入enter
    # win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)    # 释放按键
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 360拦截了虚拟按键,可以添加信任或者关闭360
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


open_by_grab()
