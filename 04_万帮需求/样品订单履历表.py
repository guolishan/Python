import datetime
import os
import openpyxl
import pandas as pd
import psycopg2


def get_data():
    global df
    # 当前时间
    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----开始执行...")

    # 连接DB执行SQL取数
    df = conn_db()

    # 显示所有列和列
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


def conn_db():
   # psycopg2 postgreSQL包
    # UAT 环境
    # conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
    #                         host="172.16.1.12",port="5432")

    # 生产环境
    conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
                            host="172.16.1.18",port="5433")
    cur = conn.cursor()

    sql = "SELECT b.wt_project_id,c.project_code,c.product_count,c.project_name,a.wti_item_code,c.product_name,c.product_standard,a.wti_operate_code,a.wti_operate_type,a.wti_operate_time,c.pm_memo, a.wti_item_sn, a.wti_doc_type " \
          "FROM T_WIP_TRACKING b LEFT JOIN T_WMS_TASK_LOG a on a.wti_item_sn = b.wt_sn " \
          "INNER JOIN T_PM_PROJECT_BASE c on b.wt_project_id = c.project_id " \
          "WHERE wti_item_sn in (SELECT wt_sn from T_WIP_TRACKING  WHERE wt_mo_number like 'YP%')" \
          "AND a.wti_wh_code = '0108' and a.wti_doc_type is not null"

    cur.execute(sql)

    data = cur.fetchall()

    columnDes = cur.description #获取连接对象的描述信息

    columnNames = [columnDes[i][0] for i in range(len(columnDes))]

    df = pd.DataFrame([list(i) for i in data],columns=columnNames)

    conn.close()

    return df


# 数据处理
def process_data():
    global df,df_new

    df_new = pd.DataFrame(columns=["wt_project_id","product_count", "wti_item_sn", "project_code", "project_name", "wti_item_code", "product_name", "product_standard", "gr_time","gi_time", "pm_memo"])

    # 去除重复行数据 keep:'first':保留重复行的第一行，'last':保留重复行的最后一行,False：删除所有重复行
    df1 = df.drop_duplicates(
        subset = ['wti_item_sn'],  # 去重列，按这些列进行去重
        keep = 'first'  # 保存第一条重复数据
    )

    # 去除重复行数据 keep:'first':保留重复行的第一行，'last':保留重复行的最后一行,False：删除所有重复行
    df = df.drop_duplicates(
        subset=['wt_project_id','wti_item_sn','wti_doc_type'],  # 去重列，按这些列进行去重
        keep='last'  # 保存第一条重复数据
    )

    print('---' * 50)
    print(df1)
    #
    # print('---' * 50)
    # print(df)

    flg_gi = ''
    flg_gr = ''

    # 数据遍历
    for index1, row1 in df1.iterrows():
        s1 = pd.Series([row1['wt_project_id'],row1['project_code'],row1['product_count'],row1['project_name'],row1['wti_item_code'],row1['product_name'],row1['product_standard'],row1['pm_memo'],row1['wti_item_sn']],index = ['wt_project_id','project_code','product_count','project_name','wti_item_code','product_name','product_standard','pm_memo','wti_item_sn'] )
        flg_gi = ''
        flg_gr = ''
        if row1['wt_project_id'] == 'YP-BPM-2012017':
            print('aa')
        for index, row in df.iterrows():
            if row1['wti_item_sn'] == row['wti_item_sn']:
                if row['wti_doc_type'] == 'DJ06' and flg_gr == '':    # 入库
                    flg_gr = 'X'
                    s2 = pd.Series([row['wti_operate_time']],index = ['gr_time'])
                    s1 = s1.append(s2)
                elif( row['wti_doc_type'] == 'DJ14' or row['wti_doc_type'] == 'DJ16' or row['wti_doc_type'] == 'DJ11' or row['wti_doc_type'] == 'DJ10' ) and flg_gi == '':    # 出库或者调拨或者销售发货
                    flg_gi = 'X'
                    s2 = pd.Series([row['wti_operate_time']],index = ['gi_time'])
                    s1 = s1.append(s2)


        # print('---' * 50)
        # print(s1)
        # print('---' * 50)
        # print(df_new)

        df_new = df_new.append(s1,ignore_index=True)

    # 标题重命名
    df_new.rename(columns={"wt_project_id": "订单号", "project_code": "项目编号", "product_count": "订单数量", "project_name": "项目名称", "wti_item_code": "料号","product_name": "料号名称",
                       "product_standard": "规格型号","gr_time": "入库时间","gi_time": "出库时间","pm_memo": "订单备注","wti_item_sn": "产品SN"}, inplace=True)

    df = df_new

# 数据输出到Excel
def output_data():
    global  df
    # 数据输出
    os.makedirs('D:/MES报表',exist_ok=True)

    time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    OUT_DIR = 'D:/MES报表/' + "样品订单履历表_" + time_str + ".xlsx"

    writer = pd.ExcelWriter(OUT_DIR)
    df.to_excel(writer,index=False)
    writer.save()

    print("文件已经保存文件到:{} ".format(OUT_DIR))

    now_str= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"----{now_str}----程序结束执行...")

if __name__ == '__main__':
    get_data()
    process_data()
    output_data()
    input("please input any key to exit!")