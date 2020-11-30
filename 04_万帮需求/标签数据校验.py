import datetime
import os
import sqlite3

from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

global db_path,g_label_id

db_path = f'D:/MES(误删)'

class Stats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 从文件中加载UI定义
        self.ui = QUiLoader().load('../00_项目文件库/1_UI/Label.ui')
        # self.ui = QUiLoader().load('Label.ui')

        self.create_table()
        # 初始化控件
        self.init_ui()
        #回车键或return按键按下信号
        self.ui.lineEdit.returnPressed.connect(self.check_duplicated)

    def init_ui(self):
        self.ui.textBrowser.clear()
        self.ui.textBrowser.append('条码扫描记录：')

    # 创建表
    def create_table(self):
        global db_path,g_label_id

        if not os.path.exists(db_path):
            os.makedirs(db_path,exist_ok=True)

        db_path = db_path + '/label.db'

        print(db_path)

        conn = sqlite3.connect(db_path)
        print("Opened database success")

        cur = conn.cursor()
        q_sql = "select count(1) from sqlite_master where type='table' and name = 't_label_log'"
        c_sql = "create table t_label_log (id integer primary key autoincrement,label_id varchar(100) not null,create_time date)"
        cur.execute(q_sql)

        result = cur.fetchone()
        if result[0] == 0:
            cur.execute(c_sql)
            print("create success")
        else:
            print("table already exists")

        conn.commit()
        conn.close()

    def check_duplicated(self):
        global db_path,g_label_id

        g_label_id =  self.ui.lineEdit.text()
        self.ui.lineEdit.clear()

        l_result = ''

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("select * from t_label_log where label_id=:temp", {"temp": g_label_id})

        result = cur.fetchone()

        if result == None:
            # 条码规则校验
            if len(g_label_id) != 21: #1.1 检验条码位数等于21位l_result = '标签：' + g_label_id + '---> OK'
                QMessageBox().warning(self, '提示', '条码长度不符合规定')
                l_result = '标签：' + g_label_id + '---> NG , 条码长度不符合规定'
            elif g_label_id[0:8] not in('10140290','10140150','10141300','10141310','10141340',
                                        '10141350','10141120','10141100','10141130','10141440','10141950','10141960','10140280','10140300','10139780'):
                QMessageBox().warning(self, '提示', '条码前8位不符合规定')
                l_result = '标签：' + g_label_id + '---> NG , 条码前8位不符合规定'
            elif g_label_id[11:17] != '200185':
                QMessageBox().warning(self, '提示', '客户代码不对')
                l_result = '标签：' + g_label_id + '---> NG , 客户代码不对'
            elif g_label_id[17] != 'A':
                QMessageBox().warning(self, '提示', '条码第18位不符合规定')
                l_result = '标签：' + g_label_id + '---> NG , 条码第18位不符合规定'
            elif g_label_id.find('I')>=0 or g_label_id.find('O')>=0:
                QMessageBox().warning(self, '提示', '条码包含I或者O不符合规定')
                l_result = '标签：' + g_label_id + '---> NG , 条码包含I或者O不符合规定'
            else:
                cur.execute('INSERT INTO t_label_log (label_id,create_time) VALUES (?,?)', (g_label_id, datetime.datetime.now()))
                l_result = '标签：' + g_label_id + '---> OK'
        else:
            QMessageBox().warning(self, '提示', '标签重复')
            l_result = '标签：' + g_label_id + '---> NG'


        self.ui.textBrowser.append(l_result)

        conn.commit()
        conn.close()


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

    except Exception as e:
        print(e)