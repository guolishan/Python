import re

# text = '<h2>国家强大 人民强大 aoligei<h2>'
# pattern = '<h2>(.*)(ei)<h2>'
#
# # match 匹配 ， 只能够从头开始匹配
# # search 搜寻 ， 可以从字符串任意位置开始匹配
#
# # . 除换行符的任意字符 DOTALL，如果需要匹配换行符，需要添加一个Flag,即：re.S
#
# tittle = re.match(pattern,text,re.S)
#
# # * 代表着前面的字符出现 0次或者多次
# # (...) 分组匹配, 分组后面可加数量词,从左到右,每遇到一个 ( 编号+1) 分组后面可加数量词 ， 从左到右，
# # ^ 匹配字符串开头， 多行匹配每一行开头
# # $ 匹配字符串末尾，多行匹配每一行末尾
#
#
#
#
# # match 函数如果没有匹配到，返回None
#
#
#
# print( f'tittel的值: { tittle }')
#
# print(f'Group(0)的值：{tittle.group(0)}')
#
# print(f'Group(1)的值：{tittle.group(1)}')
#
# print(f'Group(2)的值：{tittle.group(2)}')

# text = 'I  want wo mamamiya 12'
# pattern = '[\w]+'
#
# words = re.findall(pattern,text)
#
# print(words)

# text = 'I  want wo mamamiya 12'
# pattern = '[\w]+'
#
# words = re.finditer(pattern,text)
#
# for item in words:
#     print(item)
#     print(item.group(0))
#     print('--'*50)
#
# text = 'I  want wo mamamiya 12'
# pattern = '[\w]+'
# words = re.findall(pattern,text)
# print(words)
#
# print('-'*50)
#
# pat = re.compile(pattern)
# words = pat.findall(text)
# print(words)

# s = r'test\tddd'
# s2 = 'test\tddd'
# print(s)
# print(s2)

line = '本科'

age = re.search(r'大专|本科', line)
print(age)
if age:
    age = age.group(0)
    print(age)
