import sys

import pandas as pd
import psycopg2
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox
from PySide2.QtWidgets import QFileDialog

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
        self.ui = QUiLoader().load('../00_项目文件库/1_UI/MES_Table.ui')

        # self.ui = QUiLoader().load('APS_Tool.ui')

        # 初始化table控件
        self.init_ui()

        #显示所有列
        pd.set_option('display.max_columns', None)
        # #显示所有行
        pd.set_option('display.max_rows',None)


        # 按钮事件
        self.ui.Button_Upload.clicked.connect(self.handleUpload)

    # 初始化table控件
    def init_ui(self):
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
            ['Table 名称','数据条目数', '更新结果',])


    def handleUpload(self):
        global df,ser_pro_des,ser_pro_id,pro_len,g_type_id

        # 上传按钮禁用，防止多次连续点击
        self.ui.Button_Upload.setEnabled(False)

        def insert_data(series):
            sql = "insert into sy_dict_val values(F_C_GETNEWID(),%s,%s,%s,%s,%s,%s);"
            cur.execute(sql,(series[0],series[1],series[2],series[3],series[4],series[5]))


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
        df = pd.read_excel(file_path, header=0,sheet_name= "维修-不良原因")

        # 针对空格进行数据填充
        df = df.fillna(method='pad',axis=0)

        # 获取表头信息
        ser_pro_id = pd.Series(list(df.columns))

        # 获取表头长度
        pro_len = len(ser_pro_id) - 4

        try:
            # # UAT环境
            # conn = psycopg2.connect(database="n2db",user="n2admin",password="123",
            #                         host="172.16.1.12",port="5432")

            # 生产环境
            conn = psycopg2.connect(database="n2db",user="n2admin",password="N2ADMIN",
                                host="172.16.1.18",port="9999")

            cur = conn.cursor()
        except:
            QMessageBox().warning(self, '提示', '连接数据库失败')
            return False
        else:
            print(df)
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