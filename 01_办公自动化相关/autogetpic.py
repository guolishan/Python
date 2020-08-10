import sys
import time

from PIL import Image
from src.main.dosthauto import autologin
from src.main.imagehandle import imagehandle

# 路径
addr = sys.path[0] + "\\resources"


def get_pic(driver, path):
    # 截全屏
    driver.save_screenshot(addr + "\whole.png")
    # 定位验证码
    img_element = driver.find_element_by_id("safecode")
    location = img_element.location
    size = img_element.size
    code_range = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))
    # 使用Image的crop函数，从截图中再次截取我们需要的区域
    img = Image.open(addr+"\whole.png")
    frame = img.crop(code_range)
    # 转化为灰度图
    imgry = frame.convert('L')
    # 获取图片中的出现次数最多的像素，即为该图片的背景
    max_pixel = imagehandle.get_threshold(imgry)
    # 将图片进行二值化处理
    table = imagehandle.get_bin_table(threshold=max_pixel)
    out = imgry.point(table, '1')
    # 去掉图片中的噪声（孤立点）
    out1 = imagehandle.cut_noise(out)
    # 去掉边框
    out2 = imagehandle.remove_frame(out1, 1)
    out2.save(path)
    # 点击验证码
    driver.find_element_by_id('safecode').click()


def pic_start():
    driver = autologin.open_chrome()
    for i in range(100, 200):
        print("第%d次获取验证码" % (i+1))
        path = "E:\py-file\py-pic\\test\\%d.jpg" % (i+1)
        get_pic(driver, path)
        time.sleep(1)
    print(">>>获取验证码结束")
    driver.quit()
