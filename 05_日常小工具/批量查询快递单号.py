import re

import bs4
import pandas as pd
import requests
import xlwt
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox
from PySide2.QtWidgets import QTableWidgetItem, QFileDialog


class Stats(QWidget):
    def __init__(self, parent=None):
        super(Stats, self).__init__(parent)

        self.ui = QUiLoader().load('../00_项目文件库/1_UI/Logistics.ui')

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
        self.ui.table.setColumnWidth(1, 160)
        # 设定第2列的宽度为 100像素
        self.ui.table.setColumnWidth(2, 160)
        self.ui.table.setColumnWidth(3, 800)

        self.ui.table.horizontalHeader().setStretchLastSection(True)

    # 批量查询
    def handleCalc(self):
        self.clear_data()

        df = pd.read_clipboard(header=None)


        for index, row in df.iterrows():
            doc_no = row[0]

            result = self.search_data(doc_no)

            if result.empty:
                continue
            else:
                self.display_data(result)

    # 单个快递号查询
    def handleCalc_single(self):
        self.clear_data()
        doc_no = self.ui.lineEdit.text()
        result = self.search_data(doc_no)

        if result.empty:
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

    #查询快递单号
    def search_data(self,doc_no):
        doc_no = str(doc_no)

        if doc_no[0:2] == '55': #百世汇通
            express = 'htky'
            express_name = '百世汇通'
        elif doc_no[0:2] == '99': #顺丰
            express = 'sfexpress'
            express_name = '顺丰'
        elif doc_no[0:2] == '99': #韵达
            express = 'yunda'
            express_name = '韵达'
        elif doc_no[0:2] == '99': #申通
            express = 'sto'
            express_name = '申通'
        elif doc_no[0:2] == '99': #圆通
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

        url = 'http://m.46644.com/express/result.php?typetxt=%D6%D0%CD%A8&type=' + express + '&number=' + doc_no

        response = requests.get(url)
        response.encoding = 'GB18030'
        response = response.text
        soup = bs4.BeautifulSoup(response, 'html.parser', from_encoding="utf8")


        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        df = pd.DataFrame(columns=('doc_no','com', 'time', 'status'))

        list_status = []
        list_com = []
        list_time = []
        list_doc_no = []

        for i in soup.findAll(name='div', attrs={'class': 'icontent'}):
            list_status.append(i.get_text())
            list_com.append(express_name)
            list_doc_no.append(doc_no)

        for i in soup.findAll(name='div', attrs={'class': 'itime'}):
            str1 = str(i)
            pattern = '<div class="itime">(.*)(<br/>)(.*)(</div>)'

            date = re.match(pattern, str1)

            try:
                date_str = date.group(1) + ' ' + date.group(3)
            except Exception as e:
                print(e)

            list_time.append(date_str)


        df['doc_no'] = list_doc_no
        df['com'] = list_com
        df['time'] = list_time
        df['status'] = list_status

        return df

    # 显示快递结果
    def display_data(self,result):
        i = 0
        for index, row in result.iterrows():

            self.ui.table.insertRow(i)

            item = QTableWidgetItem('时间')
            item.setText(str(row['time']))
            self.ui.table.setItem(i, 2, item)

            item = QTableWidgetItem('物流状态')
            item.setText(str(row['status']))
            self.ui.table.setItem(i, 3, item)

            item = QTableWidgetItem('快递单号')
            item.setText(str(row['doc_no']))
            self.ui.table.setItem(i, 0, item)

            item = QTableWidgetItem('快递公司')
            item.setText(str(row['com']))
            self.ui.table.setItem(i, 1, item)

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
        stats = Stats()
        stats.ui.show()
        app.exec_()
        app.quit()

    except Exception as e:
        print(e)