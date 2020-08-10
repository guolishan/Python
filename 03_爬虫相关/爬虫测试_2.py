# 使用Ajax技术，需要在Network的XHR的General可以看到URL，且使用Post方法调用
import json

import requests

url = 'https://fanyi.baidu.com/sug'

form = {
    'kw': '小孩',
}

# 这里需要使用post方法，之前都是get方法
# 爬虫第三步
response = requests.post(url,data = form)


# 定位数据，爬虫第四步：
print(response.text)
# Json 是一个包，函数loads的作用是输入一个字符串，输出整个json字符串的Python类型数据
json_dict = json.loads(response.text)

print(json_dict)

print(type(json_dict))

for key,value in json_dict.items():
    print (f'key:{key}, value:{value}')

# 爬虫第五步： - 存储数据


# translated = json_dict['data'][0]['v']
# print('翻译后的内容是：',translated )

#列表循环
for value in json_dict['data']:
    translated = value['v']
    print('翻译后的内容是：',translated )

# with open('baidu.html','wb') as f:
#     f.write(response.content)
