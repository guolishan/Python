# 直接在Network的General可以看到URL，且使用Get方法调用
import requests

url = 'https://www.xicidaili.com/nn'

# 添加请求头信息，字典方式写入请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

# 通过某个函数获取url对应的返回值（HTML）

# response = requests.get(url,headers = headers)

response = requests.get(url,verify = False ,headers = headers)


# response.encoding = 'UTF-8"'

# response.content 的类型是Byte
# response.text 的类型是String

# response.text 等价于 response.content.decode('UTF-8')

# print(response.text)
#
# print(response.content.decode('UTF-8'))

# 保存html信息到文件
with open('../00_项目文件库/2_File/xicidail.html', 'wb') as f:
    f.write(response.content)