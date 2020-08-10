import os


# 自动杀死端口
def kill_port(port):
    res = ''
    # 查找端口的pid
    find_port= f'netstat -aon | findstr {port}'
    port_result = os.popen(find_port)
    port_text = port_result.read()
    if port_text == '':
        res = f'找不到{port}端口'
    else:
        pid= port_text [-5:-1] # TODO 12345这样的获取不对
        # 杀死占用端口的pid
        find_kill= f'taskkill -f -pid {pid}'
        kill_result = os.popen(find_kill)
        kill_text = kill_result.read()
        res = f'结果:{kill_text}'
    return res


# 处理输入的端口号handle_input(handle_str):
    input_list = handle_str.split(',')
    for item in input_list:
        item_str = item.strip()
        if item_str.isdigit():
            text = kill_port(item_str)
            print(text)
        else:
            print(f'{item_str}不是端口号')
    print("\r")


# 输入端口，自动杀死
if __name__ == '__main__':
    for i in range(0, 10):
        input_str = input(f'输入要杀死的端口,多个端口用英文逗号分格(输入end结束):')
        if input_str == 'end':
            break
        else:
            handle_input(input_str)