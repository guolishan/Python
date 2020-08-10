import random

import itchat
import requests


def get_response(msg):
    # 构造了要发送给服务器的数据
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    # noinspection PyBroadException
    try:
        r = requests.post(api_url, data=data).json()
        return r.get('text')
    except Exception:
        return


# 注册获取别人发来的信息方法
@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing', 'Picture'])
def tuling_reply(msg):
    if msg.User["NickName"] == '浩':
        pass
    else:
        print(msg.User['NickName'] + ":" + msg['Text'])
        robots = ['——By机器人小陈', '——By机器人浩浩', '——By反正不是本人']
        reply = get_response(msg['Text']) + random.choice(robots)   # 调取图灵机器人获取回复
        print(reply)
        return reply


@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)    # 群消息的处理
def print_content(msg):
    if msg.User["NickName"] == '相亲互助群':    # 可以加 or msg.User["NickName"]=='你希望自动回复群的名字'
        print(msg.User['NickName'] + ":" + msg['Text'])
        robots = ['——By这个好玩么', '——By robot 浩浩', '——By不是本人']
        reply = get_response(msg['Text']) + random.choice(robots)
        print(reply)
        return reply
    else:
        pass


if __name__ == '__main__':
    KEY = '04f44290d4cf462aae8ac563ea7aac16'
    itchat.auto_login()
    itchat.run()
