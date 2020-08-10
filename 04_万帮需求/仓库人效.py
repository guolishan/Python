# 需求描述：按照员工维度统计员工操作单据的时长，监控仓库人工效率
# t_wms_receive_detail 入库明细表
# t_wms_outstock_detail 出库明细表
# t_wms_allot_detail 调拨明细表
# 以单据+料号的维度统计：开始时间 = 操作人的第一笔时间，结束时间 = 交接人的最后一笔时间；
# 如果单据+料号，没有交接人，则以第二颗物料的第一笔发料时间作为上一颗物料的结束时间
# 有可能是abc都备好后才一起交接，加个判断交接时间，如果交接时间是在下一个料号开始时间以后的按下一个料号的开始时间当成上个料的结束时间，否则已交接时间作为这笔物料的结束时间

import copy
import datetime
import os
import sys
import time

import numpy as np
import pandas as pd
import psycopg2
from PySide2.QtCore import Qt, QDate
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox

global df,exclude_list,df_new,total_qty,exe_flag,df_user,current_ser,total_qty,exe_flag,current_ser1

class Stats(QWidget):
    def __init__(self, parent=None):
        super(Stats, self).__init__(parent)
        self.ui = QUiLoader().load('../00_项目文件库/1_UI/WM_Op.ui')
        # self.ui = QUiLoader().load('WM_Op.ui')
        # 初始化窗体相关控件
        self.init_ui()
        # 按钮事件
        self.ui.button1.clicked.connect(self.handleCalc)

    # 初始化窗体控件
    def init_ui(self):
        self.ui.dateFrom.setDate(QDate.currentDate().addDays(-7))
        self.ui.dateTo.setDate(QDate.currentDate())

        self.ui.dateFrom.setCalendarPopup(True)
        self.ui.dateTo.setCalendarPopup(True)

        self.ui.dateFrom.setDisplayFormat("yyyy/MM/dd")
        self.ui.dateTo.setDisplayFormat("yyyy/MM/dd")

        # 进度是 0 - 2，
        self.ui.bar.setRange(0,2)


    # 查询
    def handleCalc(self):
        global df,df_user
        # 图形界面中QTextBrowser控件框初始化
        self.ui.text.clear()
        # 有时，浏览框里面的内容长度超出了可见范围，我们在末尾添加了内容，往往希望控件自动翻滚到当前添加的这行，可以通过 ensureCursorVisible 方法来实现
        self.ui.text.ensureCursorVisible()

        self.cursor = self.ui.text.textCursor()
        self.ui.text.moveCursor(self.cursor.End)

        # 查询按钮禁用，防止多次连续点击
        self.ui.button1.setEnabled(False)

        s_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.ui.text.append("程序开始执行：{}".format(s_time))
        self.ui.text.append('------' * 20)
        QApplication.processEvents()  # 定时刷新
        time.sleep(0.000001)
        self.ui.bar.setValue(0)

        # 连接DB执行SQL取数
        df = self.conn_db()

        if df.empty:
            QMessageBox().warning(self, '提示', '没有符合条件的记录')
            self.ui.button1.setEnabled(True)
            return

        # 数据处理
        self.process_data()
        # 数据输出
        self.output()
        # 查询按钮恢复
        self.ui.button1.setEnabled(True)

    #数据处理
    def process_data(self):
        global df,exclude_list,df_new,total_qty,exe_flag

        # 初始化
        exclude_list = []
        df_new = pd.DataFrame(columns = ["wms_type","wrd_doc_num","wrd_item_code","qty","re_time","re_emp","hand_time","hand_emp"])
        total_qty = 0
        exe_flag = ''


        # 分别指定升序和降序
        df.sort_values(by =["wms_type","wrd_doc_num","re_time","wrd_item_code","hand_time"],ascending=[True, True,True,True,True],inplace=True)
        df = df.reset_index(drop=True)  # drop=True表示删除原索引，不然会在数据表格中新生成一列'index'数据

        #显示所有列
        # pd.set_option('display.max_columns', 3000)
        #
        # #显示所有行
        # pd.set_option('display.max_rows',3000)

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)


        # print(df)

        def cal_time(strart_time,end_time):

            #strptime 转 dateTime
            strart_time1 = strart_time
            end_time1 = end_time

            try:
                #转字符串的转换，用户储存到文本或者数据库
                start_time1 = datetime.datetime.strptime(str(strart_time1),"%Y-%m-%d %H:%M:%S.%f")
                end_time1 = datetime.datetime.strptime(str(end_time1),"%Y-%m-%d %H:%M:%S.%f")

                during_time = end_time1 - strart_time1
                time_gap = during_time.seconds / 60
            except Exception as e:
                time_gap = 0


            return time_gap

        def cal_date(current_ser,series,data_pre,data_next,date,date_next,time_gap1):
            start_time = series[4]
            end_time = series[4]

            if data_next[0] != current_ser[0] or data_next[1] != current_ser[1]: # 如果是换单或者换业务
                if current_ser.equals(series) and pd.isnull(current_ser[6]) != True:
                    start_time = current_ser[4]
                    end_time = current_ser[6]
                else:
                    start_time = current_ser[4]
                    end_time = series[4]

                if pd.isnull(current_ser[6]) != True:
                    end_time_str = datetime.datetime.strptime(str(series[6]),"%Y-%m-%d %H:%M:%S.%f")
                    end_time1 = datetime.datetime.strptime(str(start_time),"%Y-%m-%d %H:%M:%S.%f")

                    if start_time == end_time and end_time_str > end_time1:
                        end_time = series[6]

            elif data_next[2] != current_ser[2]: # 如果是同个业务，同一单，换物料
                start_time = current_ser[4]
                end_time = data_next[4]

                # 如果是这俩颗物料跨天操作，取当前物料的处理时间
                if date != date_next:
                    end_time = series[4]

                if current_ser.equals(series) and pd.isnull(series[6]) != True:
                    end_time = datetime.datetime.strptime(str(series[6]), "%Y-%m-%d %H:%M:%S.%f")
                    end_time1 = datetime.datetime.strptime(str(data_next[4]), "%Y-%m-%d %H:%M:%S.%f")
                    if end_time > end_time1:
                        end_time = end_time1

                if pd.isnull(series[6]) != True:
                    end_time_str = datetime.datetime.strptime(str(end_time),"%Y-%m-%d %H:%M:%S.%f")
                    end_time1 = datetime.datetime.strptime(str(series[6]),"%Y-%m-%d %H:%M:%S.%f")
                    end_time2 = datetime.datetime.strptime(str(series[4]), "%Y-%m-%d %H:%M:%S.%f")


                    if end_time1 > end_time2:
                        series[6] = series[4]

                    if end_time_str > end_time1: # 如果时间晚于交接时间，则以交接时间作为结束时间
                        end_time = series[6]


            elif date != date_next: # 如果是同个业务，同一单，同个物料，跨天操作
                if current_ser.equals(series):
                    start_time = current_ser[4]
                    end_time = current_ser[6]
                else:
                    start_time = current_ser[4]
                    end_time = series[4]

            elif time_gap1 > 60:
                start_time = current_ser[4]
                end_time = series[4]
            else:
                start_time = current_ser[4]
                end_time = current_ser[6]

            return start_time, end_time


        def analyze_data(series):
            global df,exclude_list,current_ser,df_new,total_qty,exe_flag,def_user

            i = series.name   # 获取每行数据所在的行

            if i == 84 :
                print()

            if i == 0:
                # current_ser = series   # 坑点：如果是series直接复制，只是copy对象指针，如果下次循环的值有变化的时候，gloal的值也会跟着变
                current_ser = copy.deepcopy(series) #对象拷贝，深拷贝
                data_pre = copy.deepcopy(series) #对象拷贝，深拷贝

            if i!= 0:
                data_pre = df.iloc[i-1,:]

            time_gap1 = 0

            if i <= len(df) - 2:
                # 获取下一条数据进行比对
                data_next = df.iloc[i+1,:]
                date = current_ser[4].strftime('%Y%m%d')
                date_next = data_next[4].strftime('%Y%m%d')
                # date_next2 = data_next2[4].strftime('%Y%m%d')

                # 当前行和第二行wms_type、wrd_doc_num、wrd_item_code、qty相同
                if data_next[0] == current_ser[0] and data_next[1] == current_ser[1] \
                        and data_next[2] == current_ser[2] and date == date_next:

                    time_gap1 = cal_time(series[4],data_next[4])

                    if time_gap1 < 60: # 休息或者吃饭
                        total_qty = total_qty + int(series[3])
                    else:
                        total_qty = total_qty + int(series[3])
                        series[3] = total_qty
                        (start_time,end_time) = cal_date(current_ser,series,data_pre,data_next,date,date_next,time_gap1)
                        time_gap = cal_time(start_time, end_time)
                        if time_gap > 300: # 排除异常数据
                            time_gap = 0
                        s2 = pd.Series([time_gap,start_time,end_time,'分钟'], index=['用时','开始时间','结束时间','单位'])
                        s3 = series.append(s2)
                        df_new = df_new.append(s3,ignore_index=True)
                        total_qty = 0
                        current_ser = copy.deepcopy(data_next) #对象拷贝，深拷贝
                        exe_flag = ''
                else:
                    total_qty = total_qty + int(series[3])
                    series[3] = total_qty
                    (start_time,end_time) = cal_date(current_ser,series,data_pre,data_next,date,date_next,time_gap1)
                    time_gap = cal_time(start_time, end_time)

                    if time_gap > 300:  # 排除异常数据
                        time_gap = 0

                    s2 = pd.Series([time_gap,start_time,end_time,'分钟'], index=['用时','开始时间','结束时间','单位'])

                    s3 = series.append(s2)
                    df_new = df_new.append(s3,ignore_index=True)

                    total_qty = 0
                    # exe_flag = 'X'
                    current_ser = copy.deepcopy(data_next) #对象拷贝，深拷贝
                    exe_flag = ''

            elif i == len(df) - 1:
                # 剩下最后一条数据
                data_next = series
                date = current_ser[4].strftime('%Y%m%d')
                date_next = data_next[4].strftime('%Y%m%d')

                # 当前行和第二行wms_type、wrd_doc_num、wrd_item_code、qty相同
                if data_next[0] == current_ser[0] and data_next[1] == current_ser[1] \
                        and data_next[2] == series[2] and date == date_next:

                    total_qty = total_qty + int(series[3])
                    # exclude_list.append(i+1)

                    series[3] = total_qty

                    (start_time,end_time) = cal_date(current_ser,series,data_pre,data_next,date,date_next,time_gap1)
                    time_gap = cal_time(start_time, end_time)

                    if time_gap > 300:  # 排除异常数据
                        time_gap = 0

                    s2 = pd.Series([time_gap,start_time,end_time,'分钟'], index=['用时','开始时间','结束时间','单位'])

                    s3 = series.append(s2)
                    df_new = df_new.append(s3,ignore_index=True)

                    total_qty = 0
                else:
                    series[3] = total_qty

                    (start_time,end_time) = cal_date(current_ser,series,data_pre,data_next,date,date_next,time_gap1)
                    time_gap = cal_time(start_time, end_time)

                    if time_gap > 300:  # 排除异常数据
                        time_gap = 0

                    s2 = pd.Series([time_gap,start_time,end_time], index=['用时','开始时间','结束时间'])

                    s3 = series.append(s2)
                    df_new = df_new.append(s3,ignore_index=True)

                    total_qty = 0
                    current_ser = copy.deepcopy(series) #对象拷贝，深拷贝

        # print('df-0',df)

        # 将不同版本的数据存放到不同的Data Frame
        df.apply(analyze_data,axis=1)

        # df = df.drop(exclude_list,axis=0)

        df = df_new

        # print('df-1',df)

        # 分别指定升序和降序
        df = df.sort_values(by =["wms_type","wrd_doc_num","re_time","wrd_item_code","hand_time"],ascending=[True, True,True,True,True])
        df = df.reset_index(drop=True)  # drop=True表示删除原索引，不然会在数据表格中新生成一列'index'数据

        # # 按照指定的栏位顺序重新排序，类似abap的move-corresponding to功能
        # order = ["wms_type","re_emp","wrd_doc_num","wrd_item_code","qty","开始时间","结束时间","用时","单位"]
        # df = df[order]

        # 生成透视表
        df1_pivotTable = df.pivot_table(index=["wms_type","re_emp","wrd_doc_num","wrd_item_code","单位","开始时间","结束时间"],values=['用时','qty'],aggfunc={np.sum,np.sum})

        df = df1_pivotTable

        # 为了后续的运算，columns能简化，便于处理。也就是说吧columns拍平。大家可以这么处理：
        df.columns =[s1 +'_'+ str(s2) for (s1,s2) in df.columns.tolist()]
        df.reset_index(inplace=True)

        # # 针对空格进行数据填充
        # df = df.fillna(method='ffill')
        # df = df.stack().reset_index()
        #

        # 匹配姓名
        df1 = pd.merge(df,df_user.loc[:,['re_emp','name']],how='left',on = 're_emp')
        df = df1


        # move-corresponding to
        order = ["wms_type","re_emp","name","wrd_doc_num","wrd_item_code","qty_sum","开始时间","结束时间","用时_sum","单位"]
        df = df[order]


        #标题重命名
        df.rename(columns={"wms_type":"业务类型","re_emp":"工号","name":"姓名","wrd_doc_num":"单号","wrd_item_code":"料号","用时_sum":"用时","qty_sum":"数量"}, inplace = True)

        # print(df)

        # df.loc[df['用时']==0, '用时']='时间太短，无法统计'

        df = df.drop(df[(df['用时']==0)].index)

    # 数据输出到Excel
    def output(self):
        global  df
        # 数据输出
        os.makedirs('D:/WMS报表',exist_ok=True)

        time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        OUT_DIR = 'D:/WMS报表/' + "人效报表_" + time_str + ".xlsx"

        self.ui.text.append("数据已经梳理完毕，导出Excel中...")

        QApplication.processEvents()  # 定时刷新
        time.sleep(0.000001)
        self.ui.bar.setValue(1)

        writer = pd.ExcelWriter(OUT_DIR)
        df.to_excel(writer,index=False)
        writer.save()

        QApplication.processEvents()  # 定时刷新
        time.sleep(0.000001)
        self.ui.bar.setValue(2)

        e_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.ui.text.append('------' * 20)
        self.ui.text.append("程序结束执行：{}".format(e_time))
        self.ui.text.append('------' * 20)
        self.ui.text.append("文件已经保存文件到:{} ".format( OUT_DIR))


    def conn_db(self):

        sBeginDate = self.ui.dateFrom.date().toString(Qt.ISODate)
        sEndDate = self.ui.dateTo.date().toString(Qt.ISODate)
        # psycopg2 postgreSQL包
        # UAT 环境
        # conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
        #                         host="172.16.1.12",port="5432")

        # 生产环境
        conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
                                host="172.16.1.18",port="5433")
        cur = conn.cursor()

        sql = f"(SELECT '入库' as wms_type, wrd_doc_num , wrd_item_code,wrd_current_num as qty,wrd_receive_time as re_time,wrd_receive_emp as re_emp,WRD_HANDOVER_TIME as hand_time,WRD_HANDOVER_EMP as hand_emp " \
              f"FROM T_WMS_RECEIVE_DETAIL WHERE wrd_receive_time BETWEEN '{sBeginDate}' and '{sEndDate}' LIMIT 0) " \
              f"UNION " \
              f"(SELECT '出库' as wms_type, wod_doc_num,wod_item_code, wod_outstock_num as qty,WOD_OUTSTOCK_TIME as re_time,WOD_OUTSTOCK_EMP as re_emp,WOD_HANDOVER_TIME as hand_time,WOD_HANDOVER_EMP as hand_emp " \
              f"FROM T_WMS_OUTSTOCK_DETAIL WHERE WOD_OUTSTOCK_TIME BETWEEN '{sBeginDate}' and '{sEndDate}'  and  wod_doc_num like 'PPBOM%') " \
              f"UNION " \
              f"(SELECT '调拨' as wms_type,  wad_doc_num as wod_doc_num, wad_item_code as wod_item_code,wad_allot_num as qty,WAD_ALLOT_TIME as re_time,WAD_ALLOT_EMP as re_emp,WAD_HANDOVER_TIME as hand_time,WAD_HANDOVER_EMP as hand_emp " \
              f"FROM t_wms_allot_detail WHERE WAD_ALLOT_TIME BETWEEN '{sBeginDate}' and '{sEndDate}' LIMIT 0);"


        # sql1 = "SELECT '入库' as wms_type, wrd_doc_num , wrd_item_code,wrd_current_num as qty,wrd_receive_time as re_time,wrd_receive_emp as re_emp,WRD_HANDOVER_TIME as hand_time,WRD_HANDOVER_EMP as hand_emp FROM T_WMS_RECEIVE_DETAIL WHERE wrd_doc_num = 'CGSL069549' or wrd_doc_num = 'CGSL069551'or wrd_doc_num = 'CGSL069551';"
        sql1 = "SELECT '出库' as wms_type, wod_doc_num as wrd_doc_num,wod_item_code as wrd_item_code, wod_outstock_num as qty,WOD_OUTSTOCK_TIME as re_time,WOD_OUTSTOCK_EMP as re_emp,WOD_HANDOVER_TIME as hand_time,WOD_HANDOVER_EMP as hand_emp FROM T_WMS_OUTSTOCK_DETAIL WHERE wod_doc_num = 'PPBOM00014954';"

        cur.execute(sql)

        data = cur.fetchall()

        columnDes = cur.description #获取连接对象的描述信息

        columnNames = [columnDes[i][0] for i in range(len(columnDes))]

        df = pd.DataFrame([list(i) for i in data],columns=columnNames)

        # conn.close()


        # 获取用户信息
        global df_user
        cur = conn.cursor()
        sql = 'SELECT login_name as re_emp, name from SY_USER'

        cur.execute(sql)

        data = cur.fetchall()

        columnDes = cur.description #获取连接对象的描述信息

        columnNames = [columnDes[i][0] for i in range(len(columnDes))]

        df_user = pd.DataFrame([list(i) for i in data],columns=columnNames)

        conn.close()

        return df

if __name__ == '__main__':
    try:
        app = QApplication([])
        # 加载 icon
        app.setWindowIcon(QIcon('../00_项目文件库/1_UI/logo.png'))
        # app.setWindowIcon(QIcon('logo.png'))
        stats = Stats()
        stats.ui.show()
        app.exec_()
        app.quit()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)