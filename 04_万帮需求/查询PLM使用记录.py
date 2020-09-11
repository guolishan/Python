import datetime
import os

import cx_Oracle
import numpy as np
import pandas as pd
import psycopg2

global df_user

def get_data_plm():
    global df
    # 当前时间
    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----开始执行...")

    # 连接DB执行SQL取数
    df = conn_db_plm()

    # 显示所有列和列
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

def conn_db_plm():
    # 生产环境
    conn = cx_Oracle.connect('pdmlink11/pdmlink11@172.16.1.33:1521/wind')
    cur = conn.cursor()

    df_new = pd.DataFrame(columns=["type","name", "dep", "count"])
    list_name = []
    list_dep = []
    list_count = []
    list_type = []

    # 查询创建者创建的部件数量
    sql = "SELECT COUNT(distinct a.IDA2A2),c.FULLNAME from wtpartmaster a,wtpart,wtuser c where a.ida2A2 = wtpart.ida3masterreference and wtpart.ida3d2iterationinfo = c.IDA2A2 group by c.FULLNAME"
    cur.execute(sql)
    data = cur.fetchall()
    df = pd.DataFrame([list(i) for i in data])

    for index, row in df.iterrows():
        list_name.append(row[1])
        list_count.append(row[0])
        list_type.append('部件')
        list_dep.append('')


    #根据属性部门查询成品数量
    sql_1 = "SELECT count(distinct wpm.IDA2A2),sv.value FROM WTPARTMASTER wpm LEFT JOIN WTPART wp ON wpm.IDA2A2 = wp.IDA3MASTERREFERENCE and wp.ida3b2folderinginfo = '148475' LEFT JOIN stringvalue sv ON wp.ida2a2 = sv.ida3a4 and sv.IDA3A6 = '70000' group by sv.value"
    cur.execute(sql_1)
    data = cur.fetchall()
    df_1 = pd.DataFrame([list(i) for i in data])

    for index, row in df_1.iterrows():
        list_count.append(row[0])
        list_dep.append(row[1])
        list_type.append('成品')
        list_name.append('')

    #查询创建者创建的solidworks模型数量
    sql_2 = "SELECT count(distinct wpm.IDA2A2), wu.FULLNAME FROM epmdocumentmaster wpm LEFT JOIN epmdocument wp ON wpm.IDA2A2 = wp.IDA3MASTERREFERENCE and wpm.AUTHORINGAPPLICATION = 'SOLIDWORKS' LEFT JOIN WTUSER wu ON wu.IDA2A2 = wp.IDA3D2ITERATIONINFO group by wu.FULLNAME"
    cur.execute(sql_2)
    data = cur.fetchall()
    df_2 = pd.DataFrame([list(i) for i in data])

    for index, row in df_2.iterrows():
        list_name.append(row[1])
        list_count.append(row[0])
        list_type.append('solidworks模型')
        list_dep.append('')

    #查询创建者创建的creo模型数量
    sql_3 = "SELECT count(distinct wpm.IDA2A2), wu.FULLNAME FROM epmdocumentmaster wpm LEFT JOIN epmdocument wp ON wpm.IDA2A2 = wp.IDA3MASTERREFERENCE and wpm.AUTHORINGAPPLICATION = 'PROE' LEFT JOIN WTUSER wu ON wu.IDA2A2 = wp.IDA3D2ITERATIONINFO group by wu.FULLNAME"
    cur.execute(sql_3)
    data = cur.fetchall()
    df_3 = pd.DataFrame([list(i) for i in data])

    for index, row in df_3.iterrows():
        list_name.append(row[1])
        list_count.append(row[0])
        list_type.append('creo模型数量')
        list_dep.append('')

    #查询创建者创建的升级请求数量 - 升级请求
    sql_4 = "SELECT count(distinct wpm.IDA2A2),wu.FULLNAME FROM promotionnotice wpm,WTUSER wu where wpm.ida3a7 = wu.IDA2A2 group by wu.FULLNAME"
    cur.execute(sql_4)
    data = cur.fetchall()
    df_4 = pd.DataFrame([list(i) for i in data])

    for index, row in df_4.iterrows():
        list_name.append(row[1])
        list_count.append(row[0])
        list_type.append('升级请求')
        list_dep.append('')

    # 查询创建者创建的更改请求数量 - ECR
    sql_5 = " SELECT count(distinct wpm.IDA2A2),wu.FULLNAME FROM wtchangerequest2 wpm,WTUSER wu where wpm.ida3d2iterationinfo = wu.IDA2A2 group by wu.FULLNAME"
    cur.execute(sql_5)
    data = cur.fetchall()
    df_5 = pd.DataFrame([list(i) for i in data])

    for index, row in df_5.iterrows():
        list_name.append(row[1])
        list_count.append(row[0])
        list_type.append('ECR')
        list_dep.append('')

    #查询创建者创建的更改请求数量 - ECN
    sql_6 = "SELECT count(distinct wpm.IDA2A2),wu.FULLNAME FROM wtchangeorder2 wpm,WTUSER wu where wpm.ida3d2iterationinfo = wu.IDA2A2 group by wu.FULLNAME"
    cur.execute(sql_6)
    data = cur.fetchall()
    df_6 = pd.DataFrame([list(i) for i in data])

    for index, row in df_6.iterrows():
        list_name.append(row[1])
        list_count.append(row[0])
        list_type.append('ECN')
        list_dep.append('')

    #查询创建者创建的更改请求数量 - 问题报告
    sql_7 = "SELECT count(distinct wpm.IDA2A2),wu.FULLNAME FROM WTChangeIssue wpm,WTUSER wu where wpm.ida3d2iterationinfo = wu.IDA2A2 group by wu.FULLNAME"
    cur.execute(sql_7)
    data = cur.fetchall()
    df_7 = pd.DataFrame([list(i) for i in data])

    for index, row in df_7.iterrows():
        list_name.append(row[1])
        list_count.append(row[0])
        list_type.append('问题报告')
        list_dep.append('')

    conn.close()


    df_new['type'] = list_type
    df_new['name'] = list_name
    df_new['dep'] = list_dep
    df_new['count'] = list_count


    return df_new

def get_data_hr():
    global df_user

    conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
                            host="172.16.1.12",port="5432")

    cur = conn.cursor()

    sql = "select * from t_hr_user"

    cur.execute(sql)

    data = cur.fetchall()

    columnDes = cur.description  # 获取连接对象的描述信息

    columnNames = [columnDes[i][0] for i in range(len(columnDes))]

    df_user = pd.DataFrame([list(i) for i in data], columns=columnNames)

    conn.close()

# 数据处理
def process_data():

    global df,df_new,df_user

    df2 = pd.DataFrame(columns=["type","dep", "count"])

    df_user = df_user.dropna(axis=0)  # 删除有空值的行

    # print(df)  # 用户Administrator 和 PLM 供应商要手动添加到表

    # 匹配姓名
    df1 = pd.merge(df, df_user.loc[:, ['name', 'dep_2']], how='left', on='name')

    for index, row in df1.iterrows():
        if row[0] == '成品':
            if pd.isna(row['dep']):
                row['dep'] = '未知'

            s1 = pd.Series([row['type'],row['dep'],row['count']],index=['type', 'dep', 'count'])
        else:
            if pd.isna(row['dep_2']):
                row['dep_2'] = '未知'
            s1 = pd.Series([row['type'], row['dep_2'], row['count']], index=['type', 'dep', 'count'])

        df2 = df2.append(s1, ignore_index=True)


    # print(df2)

    # return

    # 生成透视表
    df1_pivotTable = df2.pivot_table(index=["type", "dep"],
                                    values=['count'], aggfunc={np.sum})

    df = df1_pivotTable

    # 为了后续的运算，columns能简化，便于处理。也就是说吧columns拍平。大家可以这么处理：
    df.columns = [s1 + '_' + str(s2) for (s1, s2) in df.columns.tolist()]
    df.reset_index(inplace=True)

# 数据输出到Excel
def output_data():
    global  df
    # 数据输出
    os.makedirs('D:/PLM报表',exist_ok=True)

    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    OUT_DIR = 'D:/PLM报表/' + "使用记录_" + time_str + ".xlsx"

    writer = pd.ExcelWriter(OUT_DIR)
    df.to_excel(writer,index=False)
    writer.save()

    print("文件已经保存文件到:{} ".format(OUT_DIR))

    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----程序结束执行...")


if __name__ == '__main__':
    get_data_plm()
    get_data_hr()
    process_data()
    output_data()
    input("please input any key to exit!")