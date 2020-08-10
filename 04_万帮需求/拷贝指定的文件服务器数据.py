# 作用说明：
# 1. 读取Jason文件获取相关配置信息
# 2. 登入文件服务器
# 3. 将指定文件夹下面的 ‘.mot’ 和 ‘.bin’ 文件copy 到 本地电脑的指定目录下

import json
import os
import shutil
import time

# 定义一个字典对象
share_dict = {
    "share_ip": "",
    "username": "",
    "password": "",
    "src_path": "",
    "dst_path": ""
}

# 读取配置文件,注意配置文件是否 UTF-8 编码（在notepad中打开）
def read_json():
    # noinspection PyBroadException
    try:
        with open('../00_项目文件库/2_File/shareparams.json', 'r', encoding ='utf-8') as load_f:  # 传入标识符'r'表示读取文件
            load_dict = json.load(load_f, encoding='utf-8')
        share_dict.update(load_dict) # 将Jason配置表的内容更新到字典元素内
        if len(share_dict['src_path']) == 0:
            print(">>>请先填写读取路径")
            return False
        if len(share_dict['dst_path']) == 0:
            print(">>>请先填写输出路径")
            return False
        print(">>>读取shareparams.json成功")
        return True
    except Exception as err:
        print(f">>>解析shareparams.json异常,{err}")
        return False

# 登录文件服务器
def login_share():
    mount_command = rf"net use \\{share_dict['share_ip']} /user:{share_dict['username']} {share_dict['password']}"
    res = os.system(mount_command)
    if res == 0:
        print(">>>登录成功")
        return True
    else:
        print(">>>登录失败，请检查用户密码是否正确")
        return False

# 下载文件到指定目录
def download_file():
    if not login_share():
        return
    start_time = time.time()
    # noinspection PyBroadException
    try:
        # r 表示后面的后面字符串中的\\这些不进行转译
        # f 表示我们需要我们后面的变量要用格式化的方式{ }来进行变量的使用
        src_path = rf"\\{share_dict['share_ip']}\{share_dict['src_path']}" #源文件目录
        dst_path = f"{share_dict['dst_path']}" #目标目录，下载到指定的文件目录
        if not os.path.isdir(dst_path): #判断目标目录是否存在
            os.makedirs(dst_path,exist_ok=True)#如果不存在，则新增

        print(f">>>开始从[{src_path}]下载到[{dst_path}]")
        # 假如我们要获取某个目录中所有的 文件， 包括子目录里面的文件。 可以使用 os库中的walk方法
        # 比如我们要得到某个目录下面所有的子目录 和所有的文件，存放在两个列表中
        for tmp_root, tmp_dir, tmp_names in os.walk(src_path):
            for tmp_name in tmp_names:
                if tmp_name.endswith('.mot') or tmp_name.endswith('.bin'):
                    tmp_src_path = f"{tmp_root}\{tmp_name}"
                    tmp_dst_path = f"{dst_path}\{tmp_name}"

                    # # 存在则先删除
                    # if os.path.exists(tmp_dst_path):
                    #     os.remove(tmp_dst_path)

                    #拷贝文件，可以使用shutil模块的copyfile函数。
                    # 注意，如果拷贝前，文件已经存在，则会被拷贝覆盖，所以使用该函数一定要小心。
                    shutil.copyfile(tmp_src_path, tmp_dst_path)

        end_time = time.time()
        print(f">>>下载完毕，耗时:{end_time-start_time:.1f}s")
    except Exception as err:
        print(f">>>下载异常,{err}")
        return False

# 主函数
if __name__ == '__main__':
    if read_json():
        download_file()
    input(">>>按回车关闭...")