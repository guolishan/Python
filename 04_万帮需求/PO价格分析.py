import datetime
import os
import openpyxl
import pandas as pd


def get_data():
    global df_info
    # 当前时间
    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----开始执行...")

    # 从Excel 数据
    # 读取文件
    file_path = r'D:\PO\PO.xls'
    df_raw = pd.read_excel(file_path, header=0)

    # 筛选其中的某些类，产生新的Data Frame
    df_info = pd.DataFrame(df_raw, columns=['采购日期', '供应商', '物料编码', '物料名称', '采购数量', '含税单价'])

    # 显示所有列和列
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

# 数据处理
def process_data():
    global df_info,df_new,df_out

    df_out = pd.DataFrame(columns=["采购日期", "物料编码", "物料名称", "供应商", "采购数量", "含税单价","含税单价_old"])

    df_info = df_info.drop(df_info[df_info['采购日期'].isna()].index)

    # 去除重复行数据 keep:'first':保留重复行的第一行，'last':保留重复行的最后一行,False：删除所有重复行
    df1 = df_info.drop_duplicates(
        subset = ['物料编码'],  # 去重列，按这些列进行去重
        keep = 'first'  # 保存第一条重复数据
    )

    df1 = df1.drop(df1[df1['采购日期'] <= "2019/12/31"].index)

    for index, row in df1.iterrows():
        s1 = pd.Series([row['采购日期'], row['物料编码'], row['物料名称'], row['供应商'], row['采购数量'], row['含税单价'],0],
                      index=["采购日期", "物料编码", "物料名称", "供应商", "采购数量", "含税单价","含税单价_old"])

        s1['采购数量'] = 0

        df_info1 = df_info.drop(df_info[df_info['物料编码'] != row['物料编码']].index)

        for index1,row1 in df_info1.iterrows():
            row1['采购数量'] = float(row1['采购数量'].replace(",", ""))
            s1['采购数量'] = s1['采购数量'] + row1['采购数量']
            s1['含税单价_old'] = row1['含税单价']
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"----{now_str}----程序执行中...")

            if row1['采购日期'][:4] == '2019':  # 去2019年最后一笔数据即可
                break


        df_out = df_out.append(s1, ignore_index=True)


# 数据输出到Excel
def output_data():
    global  df_out
    # 数据输出
    os.makedirs('D:/PO',exist_ok=True)

    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    OUT_DIR = 'D:/PO/' + "PO分析报表_" + time_str + ".xlsx"

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