import datetime
import json
import os
import time

import schedule
import win32api
import win32con

global job_time
# 清理超过半年的文件
# 业务场景：设备上的测试文件增长量很快，目前的测试文件都会存储在设备电脑的本地，但是设备电脑硬盘容量有限，需要定期清理
def clear_file():
    # 当前时间
    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----开始执行...")
    for root_path in load_json['文件目录']:
        if root_path == '':
            continue
        # 获取文件后缀
        suffix_arr = load_json['文件格式']
        print(suffix_arr)

        # 遍历删除
        # 下面的三个变量 tmp_root, tmp_dir, tmp_names
        # tmp_root 代表当前遍历到的目录名
        # tmp_dir 是列表对象，存放当前dirpath中的所有子目录名
        # tmp_names 是列表对象，存放当前dirpath中的所有文件名

        for tmp_root, tmp_dir, tmp_names in os.walk(root_path):
            if len(tmp_names) == 0:
                continue

            for tmp_name in tmp_names:
                filename = os.path.join(tmp_root, tmp_name)
                print(tmp_name)
                # 判断文件后缀，满足要求的才能删除
                if check_suffix(suffix_arr, tmp_name):
                    print("----开始清理...")
                    # 获取时间戳 st_ctime创建时间，st_mtime修改时间
                    try:
                        create_time = int(os.stat(filename).st_ctime)
                    except Exception as err:
                        # 获取失败的当做当前时间处理，不删除
                        create_time = int(time.time())

                    # 获取当前时间
                    now_time = int(time.time())
                    # 差值
                    diff_seconds = now_time - create_time
                    # 半年 half_year_seconds = 182.5*24*60*60
                    half_year_seconds = 24* 60 * 60

                    # 判断差值大于半年则删除
                    if diff_seconds > half_year_seconds:
                        os.remove(filename)
    print("----清理完毕...")

# 检查文件后缀是否存在
def check_suffix(tmp_arr, tmp_file):
    for tmp_suffix in tmp_arr:
        # endswith() 方法用于判断字符串是否以指定后缀结尾，如果以指定后缀结尾返回True，否则返回False。可选参数"start"与"end"为检索字符串的开始与结束位置
        if tmp_file.endswith(tmp_suffix):
            return True
    return False


class AutoRun():
    def __init__(self):
        name = '清理测试设备文件'  # 要添加的项值名称
        path = load_json['程序存放路径']
        # 注册表项名
        KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        # 异常处理
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,  KeyName, 0,  win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
            win32api.RegCloseKey(key)
        except:
            print('添加失败')
        print('添加成功！')

if __name__ == '__main__':
    # 读取配置文件
    with open('../00_项目文件库/2_File/folderparams.json', 'r', encoding='UTF-8') as load_f:  # 传入标识符'r'表示读取文件
        load_json = json.load(load_f)

    # 设定开机自启动
    auto=AutoRun()

    # 设定定时作业，每分钟运行
    schedule.every().hours.do(clear_file)

    while True:
        # run_pending:运行所有可以运行的任务
        schedule.run_pending()
        time.sleep(3)