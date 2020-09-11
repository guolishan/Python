import datetime
import re

import bs4
import pandas as pd
import requests
import xlwt
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox
from PySide2.QtWidgets import QTableWidgetItem, QFileDialog

global data_flag # 批量查询的时候标识是否有数据输出
data_flag = ''


class Stats(QWidget):
    def __init__(self, parent=None):
        super(Stats, self).__init__(parent)

        self.ui = QUiLoader().load('../00_项目文件库/1_UI/Logistics.ui')
        # self.ui = QUiLoader().load('Logistics.ui')

        # 初始化table控件
        self.init_ui()

        # 回车事件
        self.ui.lineEdit.returnPressed.connect(self.handleCalc_single)

        # 按钮事件
        self.ui.Button_Search.clicked.connect(self.handleCalc)
        self.ui.Button_Down.clicked.connect(self.handleDown)

    # 初始化table控件
    def init_ui(self):
        # 设定第1列的宽度为 180像素
        self.ui.table.setColumnWidth(0, 160)
        # 设定第2列的宽度为 100像素
        self.ui.table.setColumnWidth(1, 100)
        self.ui.table.setColumnWidth(2, 100)
        # 设定第2列的宽度为 100像素
        self.ui.table.setColumnWidth(3, 160)
        self.ui.table.setColumnWidth(4, 140)
        self.ui.table.setColumnWidth(5, 700)

        self.ui.table.horizontalHeader().setStretchLastSection(True)

    # 批量查询
    def handleCalc(self):
        self.ui.Button_Search.setEnabled(False)
        global data_flag
        self.clear_data()
        df = pd.read_clipboard(header=None)

        df = df.dropna(axis=0) #删除有空值的行

        for index, row in df.iterrows():
            doc_no = row[0]
            try:
                result, no_data = self.search_data(doc_no)
            except Exception as e:
                print(e)

            result = result.drop_duplicates(
                    subset=['doc_no'],  # 去重列，按这些列进行去重
                    keep='first'  # 保存第一条重复数据
                )
            self.display_data(result)

        if data_flag != 'X':
            QMessageBox().warning(self, '提示', '没有符合条件的记录')
            self.ui.Button_Search.setEnabled(True)
            return

    # 单个快递号查询
    def handleCalc_single(self):
        self.clear_data()
        doc_no = self.ui.lineEdit.text()
        try:
            result,no_data = self.search_data(doc_no)
        except Exception as e:
            print(e)

        if no_data == 'X':
            QMessageBox().warning(self, '提示', '没有符合条件的记录')
            return

        self.display_data(result)

    def clear_data(self):
        # 每次执行的时候先清空table的数据
        self.ui.table.clearContents()

        # 遍历结果
        i = self.ui.table.rowCount()
        if i != 0:
            row = i
            while row > 0:
                self.ui.table.removeRow(row - 1)
                row = row - 1

    def cal_time(self,start_time,end_time):

        try:
            # 字符串转成时间戳dateTime
            start_time1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

            # strptime 转 dateTime
            end_time1 = datetime.datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f")

            during_time = (end_time1 - start_time1).total_seconds()
            time_gap = during_time/3600
            time_gap = format(time_gap,'.1f')

        except Exception as e:
            time_gap = 0

        return time_gap

    #查询快递单号
    def search_data(self,doc_no):
        global data_flag

        doc_no = str(doc_no)
        doc_no = doc_no.strip() #去掉左右空格

        express = ''
        express_name = ''
        no_data = ''

        df = pd.DataFrame(columns=('doc_no', 'com', 'doc_status', 'time', 'time_gap', 'status'))
        list_status = []
        list_com = []
        list_time = []
        list_doc_no = []
        list_time_gap = []
        list_doc_status = []


        if doc_no[0:2] == '55': #百世汇通 - 使用中
            express = 'htky'
            express_name = '百世汇通'
        elif doc_no[0:2] == '99': #顺丰
            express = 'sfexpress'
            express_name = '顺丰'
        elif doc_no[0:2] == '99': #韵达
            express = 'yunda'
            express_name = '韵达'
        elif doc_no[0:2] == '77': #申通 - 使用中
            express = 'sto'
            express_name = '申通'
        elif doc_no[0:2] == 'YT': #圆通 - 使用中
            express = 'yto'
            express_name = '圆通'
        elif doc_no[0:2] == '99': #中通
            express = 'zto'
            express_name = '中通'
        elif doc_no[0:2] == '99': #EMS
            express = 'ems'
            express_name = 'EMS'
        elif doc_no[0:2] == '99': #天天
            express = 'ttdex'
            express_name = '天天'
        elif doc_no[0:2] == '99': #全峰
            express = 'qfkd'
            express_name = '全峰'
        elif doc_no[0:2] == '99': #邮政
            express = 'chinapost'
            express_name = '邮政'

        if express == '':
            no_data = 'X'
            list_doc_no.append(doc_no)
            list_status.append('查询不到匹配的快递公司')
            list_com.append(' ')
            list_doc_status.append(' ')
            list_time.append(' ')
            list_time_gap.append(' ')

        else:

            url = 'http://m.46644.com/express/result.php?typetxt=%D6%D0%CD%A8&type=' + express + '&number=' + doc_no

            response = requests.get(url)
            response.encoding = 'GB18030'
            response = response.text
            soup = bs4.BeautifulSoup(response, 'html.parser', from_encoding="utf8")


            pd.set_option('display.max_rows', 500)
            pd.set_option('display.max_columns', 500)
            pd.set_option('display.width', 1000)


            for i in soup.findAll(name='div', attrs={'class': 'icontent'}):
                list_status.append(i.get_text())
                list_com.append(express_name)
                list_doc_no.append(doc_no)

                if i.get_text().find('代收')>=0 or i.get_text().find('签收')>=0 or i.get_text().find('已取件')>=0:
                    list_doc_status.append("已签收")
                else:
                    list_doc_status.append("运输中")


            for i in soup.findAll(name='div', attrs={'class': 'itime'}):
                str1 = str(i)
                pattern = '<div class="itime">(.*)(<br/>)(.*)(</div>)'

                date = re.match(pattern, str1)

                try:
                    date_str = date.group(1) + ' ' + date.group(3)
                    start_time = date_str
                    end_time = datetime.datetime.now()
                    time_gap = self.cal_time(start_time,end_time)

                except Exception as e:
                    df = []
                    no_data = 'X'
                    print(e)
                    return df,no_data

                list_time.append(date_str)
                list_time_gap.append(time_gap)

        df['doc_no'] = list_doc_no
        df['com'] = list_com
        df['time'] = list_time
        df['time_gap'] = list_time_gap
        df['status'] = list_status
        df['doc_status'] = list_doc_status

        data_flag = 'X'
        return df,no_data


    # 显示快递结果
    def display_data(self,result):
        i = 0
        for index, row in result.iterrows():

            self.ui.table.insertRow(i)

            item = QTableWidgetItem('时间')
            item.setText(str(row['time']))
            self.ui.table.setItem(i, 3, item)

            item = QTableWidgetItem('物流状态')
            item.setText(str(row['status']))
            self.ui.table.setItem(i, 5, item)

            item = QTableWidgetItem('快递单号')
            item.setText(str(row['doc_no']))
            self.ui.table.setItem(i, 0, item)

            item = QTableWidgetItem('快递公司')
            item.setText(str(row['com']))
            self.ui.table.setItem(i, 1, item)

            item = QTableWidgetItem('时差(小时)')
            item.setText(str(row['time_gap']))
            self.ui.table.setItem(i, 4, item)

            item = QTableWidgetItem('单号状态')
            item.setText(str(row['doc_status']))
            self.ui.table.setItem(i, 2, item)

            i = i + 1

    # 下载文件
    def handleDown(self):

        filename,ok2 = QFileDialog.getSaveFileName(self, "文件保存",
                                                   "C:/",
                                                   "文件类型 (*.xls *.xlsx)")

        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet')
        for line in range(self.ui.table.rowCount()): #获取当前表格共有多少行
            for row in range(self.ui.table.columnCount()): #获取当前表格共有多少列
                sheet.write(line, row, self.ui.table.item(line,row).text())

        book.save(filename)


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