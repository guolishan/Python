#-*- conding:utf-8 -*-
''''''
from  lxml import etree
import requests
import re
import time
'''
    需求分析
        1.https://sou.zhaopin.com/进入职位搜索获取职位分类列表
        2.通过分类进入职位详细列表
        3.进入职位详细信息页面
        获取详细的职位信息
    源码分析
        
    代码实现
'''

#1.获取职位分类列表 url
def get_job_cat_list(url,headers):
    r = requests.get(url,headers= headers).text
    # 解析
    index = etree.HTML(r)
    #获取分类列表的url
    job_url = index.xpath('//div[@id="search_right_demo"]/div/div/a/@href')
    #替换参数
    pattern = re.compile('jl=\d+&')
    new_job_url = [url[:-1]+pattern.sub('jl=489&',i) for i in job_url]
    return new_job_url


#2.获取职位列表
def get_job_list(url,headers):
    #发送请求
    result = requests.get(url,headers = headers).text
    #解析
    job_list = etree.HTML(result)

    #获取职位信息列表的 url
    job_url = job_list.xpath('//div[@id="newlist_list_content_table"]/table/tr[1]/td[1]/div/a[1]/@href')
    #获取下一页
    next_page = job_list.xpath('//a[@class="next-page"]/@href')

    return job_url,next_page






#3.获取职位详细信息
def get_job_info(url):
    #发送请求
    r = requests.get(url).text
    #解析
    info = etree.HTML(r)

    dic = {}

    #职位名称 zwmc         @calss = inner-left fl or @class= fl
    dic['zwmc'] = info.xpath('string(//div[@class="inner-left fl" or @class="fl"]/h1)')
    #公司名称 gsmc
    dic['gsmc'] = info.xpath('string(//div[@class="inner-left fl" or @class="fl"]/h2)')
    #公司福利 gsfl
    dic['gsfl'] = info.xpath('//div[@class="welfare-tab-box"]/span/text()')
    #职位月薪 zwyx
    dic['zwyx'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[1]/strong)')
    # gzdd
    dic['gzdd'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[2]/strong)')
    dic['fbrq'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[3]/strong)')
    dic['gzxz'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[4]/strong)')
    dic['gzjy'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[5]/strong)')
    dic['zdxl'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[6]/strong)')
    dic['zprs'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[7]/strong)')
    dic['zwlb'] = info.xpath('string(//div[@class="terminalpage-left"]/ul/li[8]/strong)')

    jobs_info = clear_none(dic)
    if jobs_info:
        jobs_infos = clear_data(jobs_info)
        save_data(jobs_infos)

#过滤
zw_lis = []
def clear_none(data):
    if data['zwmc'] == '' or data['zwmc'] in zw_lis:
        return False
    else:
        zw_lis.append(data['zwmc'])
        return data

#清洗
def clear_data(data):
    #gsfl
    data['gsfl'] = '_'.join([str(i) for i in data['gsfl']])
    #zwyx min_zwyx max_main
    patten = re.compile('\d+')
    zwyxlis = patten.findall(data['zwyx'])
    if len(zwyxlis) == 2:
        data['min_zwyx'] = zwyxlis[0]
        data['max_zwyx'] = zwyxlis[1]
        data.pop('zwyx')
    elif '面议' == data['zwyx']:
        data['min_zwyx'] = data['max_zwyx'] = 0
    else:
        data['min_zwyx'] = data['max_zwyx'] = zwyxlis[0]

    #gzdd
    data['gzdd'] = data['gzdd'].split('-')[0]
    #zprs
    data['zprs'] = data['zprs'].strip('人 ')

    #fbrq
    time_tup = time.strptime(data['fbrq'],'%Y-%m-%d %H:%M:%S')
    data['fbrq'] = time.strftime('%Y-%m-%d',time_tup)


    return data



#4.保存数据
def save_data(data):
    datas = ','.join([str(i) for i in data.values()])
    print(datas)
    with open('zlzp.csv','a+',encoding='utf-8') as file:
        file.write(datas+'\n')



if __name__=='__main__':
    #入口地址
    url = 'http://sou.zhaopin.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        # 'Referer': 'https: // www.zhaopin.com /',

    }
    with open('zlzp.csv','w',encoding='utf-8') as file:
        file.write('zwmc,gsmc,gsfl,zwyx,gzdd,fbrq,gzxz,gzjy,zdxl,zprs,zwlb\n')


    #a. get_job_cat_list 获取分类
    job_cat_list = get_job_cat_list(url,headers)
    # print(job_cat_list)
    #b.get_job_list 获取职位列表
    # for x in job_cat_list:
    job_list,next_page = get_job_list(job_cat_list[0],headers = headers)
    #
    # print(job_list)
    #c.get_job_info 获取职位详细信息
    for i in job_list:
        get_job_info(i)