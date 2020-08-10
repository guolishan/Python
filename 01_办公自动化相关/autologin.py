import os
import sys
import time

from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from src.main.imagehandle import imagehandle

# import traceback

# 路径
addr = sys.path[0]+"\\resources"


def open_chrome():
    """
    ie_driver = sys.path[0]+"\py-driver\IEDriverServer.exe"
    os.environ["webdriver.ie.driver"] = ie_driver
    driver=webdriver.Ie(ie_driver)
    """
    # 启动配置
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    # 环境配置
    chrome_driver = addr+"\chromedriver.exe"
    # os.environ["webdriver.ie.driver"] = chrome_driver
    # 打开chrome
    driver = webdriver.Chrome(chrome_driver, options=option)
    driver.get('http://ip:8980/eep/login.htm')  # 内部环境
    # 最大化谷歌
    driver.maximize_window()
    time.sleep(1)
    # 弹窗自动点击
    alert = driver.switch_to.alert
    at_text = alert.text
    print(at_text)
    alert.accept()
    return driver


def identify_code(driver):
    # 截取验证码
    driver.save_screenshot(addr+"\whole.png")
    img_element = driver.find_element_by_id("safecode")
    location = img_element.location
    size = img_element.size
    code_range = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))
    img = Image.open(addr+"\whole.png")
    frame = img.crop(code_range)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame.save(addr+"\\frame.png")
    # 识别验证码
    text = imagehandle.orc_lmj(addr + "\\frame.png")
    print("验证码:" + text)
    driver.find_element_by_id('randCode').clear()
    driver.find_element_by_id('randCode').send_keys(text)


def login(driver, name, pwd):
    # 用户名密码
    driver.find_element_by_id('parent_login_name').clear()
    driver.find_element_by_id('parent_login_name').send_keys(name)
    driver.find_element_by_id('ext-comp-1002').clear()
    driver.find_element_by_id('ext-comp-1002').send_keys(pwd)
    # 验证码 登录失败会自动刷新
    identify_code(driver)
    # 登录
    driver.find_element_by_id('ext-gen29').click()
    time.sleep(1)


def ecpt_handle(driver, name, pwd):
    for i in range(0, 3):
        # 验证码失败处理
        try:
            alert1 = driver.switch_to.alert
        except NoAlertPresentException:
            time.sleep(1)
            print("登陆成功")
            break
            # traceback.print_exc()
        else:
            at_text1 = alert1.text
            if at_text1 == "验证码错误":
                alert1.accept()
                time.sleep(1)
                print("重新登录%d次" % (i+1))
                login(driver, name, pwd)
    time.sleep(3)
    print("关闭")
    driver.quit()
    del_uncfd_files()  # 删除下载的未确认文件


def del_uncfd_files():
    path = "C:\\Users\Administrator\Downloads\\"
    x = 0
    for file in os.listdir(path):
        if file.find("未确认") != -1:
            os.remove(path + file)
            x += 1
        else:
            pass
    print("共删除%d个未确认的下载文件" % x)


def auto(name, pwd):
    driver = open_chrome()
    login(driver, name, pwd)
    ecpt_handle(driver, name, pwd)


# auto("cth","789456")
