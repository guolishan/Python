# 定时切换，ALT+Tab功能
import pyautogui,time,json

# 定义一个字典对象
share_dict = {
    "time_gap": "",
}

# 读取配置文件,注意配置文件是否 UTF-8 编码（在notepad中打开）
def read_json():
    # noinspection PyBroadException
    try:
        # with open('../00_项目文件库/2_File/config.json', 'r', encoding ='utf-8') as load_f:  # 传入标识符'r'表示读取文件
        with open('config.json', 'r', encoding='utf-8') as load_f:  # 传入标识符'r'表示读取文件
            load_dict = json.load(load_f, encoding='utf-8')
        share_dict.update(load_dict) # 将Jason配置表的内容更新到字典元素内
        if len(share_dict['time_gap']) == 0:
            print(">>>请先填写切换时间")
            return False
        print(">>>读取shareparams.json成功")
        return True
    except Exception as err:
        print(f">>>config.json异常,{err}")
        return False

def timer(n):
    while True:
        print(time.strftime('%Y-%m-%d %X',time.localtime()))
        myTask()  # 执行ALT + Tab功能
        time.sleep(n)

def myTask():
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    time.sleep(.2)
    pyautogui.keyUp('alt')

if __name__ == '__main__':
    read_json()
    timer(int(share_dict['time_gap']))
