import datetime
import os
import openpyxl
import pandas as pd
import numpy as np
import glob

#批量读取excel文件并合并为一张excel
def concat_file(a):
    #如何批量读取并快速合并文件夹中的excel文件
    path1=a
    file=glob.glob(os.path.join(path1,"*.xlsx"))
    #  *.xlsx  查找文件名为.xlsx的文件 *前面可以加文字立即为通配符
    #获取文件夹里面xlsx文件的名称及路径
    print(file)
    #查看获取的路径和文件名

    list1=[ ]
    #创建一个新的空列表 以存放读取的数据
    for value in file:
        list1.append(pd.read_excel(value,index_col=None))
    #循环读取xlsx文件并添加到list1列表中 pd.read_excle(可以自定义读取的方式 )
    df=pd.concat(list1,axis=0)
    #将list1 进行纵向合并  且转换为DataFrame类型

    return df

def get_data():
    global df_info
    # 当前时间
    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----开始执行...")

    # 从Excel 数据
    # 读取文件
    file_path = r'C:\Users\SC2820\Desktop\IQC2020'
    a = r'C:\Users\SC2820\Desktop\aa'
    df_raw = concat_file(file_path)



    # 筛选其中的某些类，产生新的Data Frame
    df_info = pd.DataFrame(df_raw, columns=['物料编码', '物料名称', '厂商名称', '来料数量'])

    # 显示所有列和列
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


# 数据处理
def process_data():
    global df_info,df_new,df_out

    df_out = pd.DataFrame(columns=['序号','物料编码', '物料名称', '厂商名称', '来料数量'])

    # 去除重复行数据 keep:'first':保留重复行的第一行，'last':保留重复行的最后一行,False：删除所有重复行
    df1 = df_info.drop_duplicates(
        subset = ['物料编码','厂商名称'],  # 去重列，按这些列进行去重
        keep = 'first'  # 保存第一条重复数据
    )
    print(df_info)

    print('**'*50)
    print(df1)
    # return


    i = 0
    for index, row in df1.iterrows():
        i = i + 1
        s1 = pd.Series([row['物料编码'], row['物料名称'], row['厂商名称'], row['来料数量']],index=['物料编码', '物料名称', '厂商名称', '来料数量'])

        s1['来料数量'] = 0

        print(s1['物料编码'],s1['厂商名称'])

        df_info1 = df_info.drop(df_info[df_info['物料编码'] != s1['物料编码']].index)
        df_info1 = df_info1.drop(df_info1[df_info1['厂商名称'] != s1['厂商名称']].index)

        df_info1 = df_info1.drop(df_info1[df_info1['来料数量'].isna()].index)
        df_info1 = df_info1.drop(df_info1[df_info1['来料数量'] == ' '].index)

        for index1,row1 in df_info1.iterrows():
            s1['来料数量'] = s1['来料数量'] + int(row1['来料数量'])
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"----{now_str}----程序执行中...")

        s1['序号'] = i

        df_out = df_out.append(s1, ignore_index=True)

# 数据输出到Excel
def output_data():
    global  df_out
    # 数据输出
    os.makedirs('D:/PO',exist_ok=True)

    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    OUT_DIR = 'D:/PO/' + "IQC来料分析_" + time_str + ".xlsx"

    writer = pd.ExcelWriter(OUT_DIR)
    df_out.to_excel(writer,index=False)
    writer.save()

    print("文件已经保存文件到:{} ".format(OUT_DIR))

    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----程序结束执行...")


if __name__ == '__main__':
    get_data()
    process_data()
    output_data()
    input("please input any key to exit!")