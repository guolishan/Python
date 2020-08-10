import copy
import re
import sys

import numpy as np
import pandas as pd
import psycopg2
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem, QFileDialog

global df

class Stats(QWidget):
    def __init__(self, parent=None):
        global g_type_id
        # super().__init__(parent)
        super(Stats, self).__init__(parent)

        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('../00_项目文件库/1_UI/APS_Tool.ui')

        # self.ui = QUiLoader().load('APS_Tool.ui')

        # 初始化table控件
        self.init_ui()

        #显示所有列
        pd.set_option('display.max_columns', None)
        # #显示所有行
        pd.set_option('display.max_rows',None)

        # 回车事件
        self.ui.lineEdit.returnPressed.connect(self.handleCalc)

        # 按钮事件
        self.ui.Button_Search.clicked.connect(self.handleCalc)
        self.ui.Button_Upload.clicked.connect(self.handleUpload)
        self.ui.B1.buttonClicked.connect(self.handleButtonClicked)

    # 初始化table控件
    def init_ui(self):
        global g_type_id
        # Radio Button,设定初始默认值
        self.ui.R1.setChecked(True)
        g_type_id = '交流'

        #锁定光标到Line Edit
        self.ui.lineEdit.setEnabled (True)
        self.ui.lineEdit.setFocus ()

        # table 初始化设定
        # 设定第1列的宽度为 180像素
        # self.ui.table.setRowCount(4)  # 设定行
        self.ui.table.setColumnCount(3)  # 设定列

        # 设定第1列的宽度为 180像素
        self.ui.table.setColumnWidth(0, 60)

        # 设定第2列的宽度为 100像素
        self.ui.table.setColumnWidth(1, 260)
        self.ui.table.setColumnWidth(2, 180)

        self.ui.table.horizontalHeader().setStretchLastSection(True)

        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        self.ui.table.setHorizontalHeaderLabels(
            ['产品类型','产品系列', '系列描述',])

    #Radio Button按钮事件
    def handleButtonClicked(self):
        global g_type_id
        # 获取交流or直流
        if self.ui.R1.isChecked() == True:
            g_type_id = '交流'
        else:
            g_type_id = '直流'

    # 查询
    def handleCalc(self):
        global  g_type_id
        # 每次执行的时候先清空table的数据
        self.ui.table.clearContents()

        # 遍历结果
        i = self.ui.table.rowCount()
        if i != 0:
            row = i
            while row > 0:
                self.ui.table.removeRow(row - 1)
                row = row - 1

        result = self.Search_Data()

        if len(result) < 1:
            QMessageBox().warning(self, '提示', '没有符合条件的记录')
            return

        #标题重命名
        result.rename(columns={"type_id":"产品类型","matnr_id":"系列代码","matnr_des":"名称"}, inplace = True)

        # result = result.drop_duplicates()


        i = 0
        for indexs in result.index:
            self.ui.table.insertRow(i)

            a1 = g_type_id
            a2 = result.loc[indexs].values[0]
            a3 = result.loc[indexs].values[1]

            item = QTableWidgetItem('产品类型')
            item.setText(a1)
            self.ui.table.setItem(i, 0 , item)

            item = QTableWidgetItem('产品系列')
            item.setText(a2)
            self.ui.table.setItem(i, 1 , item)

            item = QTableWidgetItem('系列描述')
            item.setText(a3)
            self.ui.table.setItem(i, 2 , item)

            i = i + 1

    def Search_Data(self):
        global g_type_id
        input_var = str(self.ui.lineEdit.text()).upper()
        c_list = re.split(",|，", input_var)

        # df_sum = pd.DataFrame(columns = ["type_id","family_id","product_id","matnr_id","family_desc","product_des","matnr_des","matnr_value"])

    # 打开数据库连接
        try:
            # UAT环境
            conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
                                    host="172.16.1.12",port="5432")
            cur = conn.cursor()
        except:
            QMessageBox().warning(self, '提示', '连接数据库失败')
            return False
        else:
            try:
                j = 0
                for c in c_list:
                    j = j+ 1
                    sql = f"SELECT distinct(matnr_id),matnr_des FROM t_aps_product WHERE product_des like '%{c}%' and matnr_value <> 'X' and type_id = '{g_type_id}';"
                    cur.execute(sql)
                    data = cur.fetchall()

                    columnDes = cur.description #获取连接对象的描述信息
                    columnNames = [columnDes[i][0] for i in range(len(columnDes))]
                    data = pd.DataFrame([list(i) for i in data],columns=columnNames)

                    if j == 1:
                        data_sum = data
                    else:
                        data_sum = pd.concat([data_sum,data])


                cur.close()
            except Exception as e:
                print(e)

        conn.close()

        # 生成透视表
        data_sum['qty'] = 1
        df1_pivotTable = data_sum.pivot_table(index=["matnr_id","matnr_des"],values=['qty'],aggfunc= np.sum)
        # 为了后续的运算，columns能简化，便于处理。也就是说吧columns拍平。大家可以这么处理：
        df1_pivotTable.columns =[s1 for s1 in df1_pivotTable.columns.tolist()]
        df1_pivotTable.reset_index(inplace=True)
        data_sum = df1_pivotTable

        if j >=2:
            print(j)
            data_sum = data_sum.drop(data_sum[(data_sum.qty < j )].index)

        return data_sum

    def create_table(self):
        # 打开数据库连接
        try:
           # UAT环境
           conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
                                host="172.16.1.12",port="5432")
           cur = conn.cursor()
        except:
           QMessageBox().warning(self, '提示', '连接数据库失败')
           return False
        else:
            try:
             # 使用cursor()方法获取操作游标
               cursor = conn.cursor()
               sql = f"CREATE TABLE IF NOT EXISTS T_APS_PRODUCT( type_id char(2) not null, family_id CHAR(20) NOT NULL, product_id CHAR(20) NOT NULL ,matnr_id char(100) not null , family_desc CHAR(100),product_des CHAR(100),matnr_des char(100), matnr_value char(1));"
               cur.execute(sql)
               conn.commit()
               cur.close()
            except Exception as e:
                print(e)

        conn.close()

        return True


    def handleUpload(self):
        global df,ser_pro_des,ser_pro_id,pro_len,g_type_id

        # 上传按钮禁用，防止多次连续点击
        self.ui.Button_Upload.setEnabled(False)

        def insert_data(series):
            global ser_pro_des,ser_pro_id,pro_len,g_type_id

            i = series.name   # 获取每行数据所在的行

            if i == 0: #获取第2行的系列描述
                ser_pro_des = copy.deepcopy(series)

            if i >= 1:
                for j in range(pro_len):
                    num = j + 4
                    # print('交流',series[1],series[3],ser_pro_id[num],series[0],series[2],ser_pro_des[num],series[num])

                    # sql = "insert into t_aps_product values('交流',{series[1]},{series[3]},{ser_pro_id[num]},{series[0]},{series[2]},{ser_pro_des[num]},{series[num]});"
                    sql = "insert into t_aps_product values(%s,%s,%s,%s,%s,%s,%s,%s);"

                    cur.execute(sql,(g_type_id,series[1],series[3],ser_pro_id[num],series[0],str(series[2]).upper(),ser_pro_des[num],series[num]))

        if self.create_table() == True:
            # 用sep来指明分隔符， sep和delim_withspace两个参数不能同时用
            # 我将',,'作为分隔符，因为我的行里面出现‘,,’的概率基本没得，所以避免了这个问题
            # df=pd.read_clipboard(encoding='utf-8',engine='python',error_bad_lines=False)
            file_path, _ = QFileDialog.getOpenFileName(
                self.ui,  # 父窗口对象
                "选择你要上传的Excel文件",  # 标题
                r"C:\\Users\\dell\\Desktop\\",  # 起始目录
                "文件类型 (*.xls *.xlsx)"  # 选择类型过滤项，过滤内容在括号中
            )
             # 读取文件
            df = pd.read_excel(file_path, header=0,sheet_name= "交流产品(Update)")

            # 针对空格进行数据填充
            df = df.fillna(method='pad',axis=0)

            # 获取表头信息
            ser_pro_id = pd.Series(list(df.columns))

            # 获取表头长度
            pro_len = len(ser_pro_id) - 4

            try:
                # UAT环境
                conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
                                        host="172.16.1.12",port="5432")
                cur = conn.cursor()
            except:
                QMessageBox().warning(self, '提示', '连接数据库失败')
                return False
            else:
                df.apply(insert_data,axis=1)

            cur.close()
            conn.commit()
            conn.close()

            QMessageBox().warning(self, '提示', '数据上传成功！')

        # 上传按钮解禁，防止多次连续点击
        self.ui.Button_Upload.setEnabled(True)
            # self.df_to_excel()

    def df_to_excel(self):
        global df
        writer = pd.ExcelWriter('APS_data.xlsx')
        df.to_excel(writer,index=False)
        writer.save()

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