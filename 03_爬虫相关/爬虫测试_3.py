# 爬取微博信息
import json

import requests
from w3lib.html import remove_tags  # 去除标签的包

base_url = 'https://m.weibo.cn/api/container/getIndex?is_all[]=1&is_all[]=1&jumpfrom=weibocom' \
           '&type=uid&value=6705323404&containerid=1076036705323404&since_id={}'

# url = 'https://m.weibo.cn/api/container/getIndex?is_all[]=1&is_all[]=1&jumpfrom=weibocom' \
#       '&type=uid&value=6705323404&containerid=1076036705323404&since_id=4513440885252026'

# 因为微博这个页面不是透过page来翻页，而是结尾指定下页的since id 来翻页
# 下面这3条代码是since_id 的初始化工作
response = requests.get(base_url)
res_dict = json.loads(response.text)
since_id  = res_dict['data']['cardlistInfo']['since_id']


for i in range(10):

    url = base_url.format(since_id)
    response = requests.get(url)
    res_dict = json.loads(response.text)

    # 每次翻页后都会在当前页指定下页的since_id
    since_id = res_dict['data']['cardlistInfo']['since_id']

    # 解析我们要获取的内容
    cards = res_dict['data']['cards']
    for card in cards:
        if 'mblog' in card:
            text = remove_tags(card['mblog']['text'])
            print(text)
            print('-'*50)
