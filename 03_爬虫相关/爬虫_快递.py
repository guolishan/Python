# 爬取快递信息
import json

import requests
import xlwt
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox
from PySide2.QtWidgets import QTableWidgetItem, QFileDialog
from w3lib.html import remove_tags  # 去除标签的包


class Stats(QWidget):
    def __init__(self, parent=None):
        super(Stats, self).__init__(parent)

        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('Logistics.ui')

        # 初始化table控件
        self.init_ui()

        # 回车事件
        self.ui.lineEdit.returnPressed.connect(self.handleCalc)

        # 按钮事件
        self.ui.Button_Search.clicked.connect(self.handleCalc)
        self.ui.Button_Down.clicked.connect(self.handleDown)

    # 初始化table控件
    def init_ui(self):
        # 设定第1列的宽度为 180像素
        self.ui.table.setColumnWidth(0, 180)
        # 设定第2列的宽度为 100像素
        self.ui.table.setColumnWidth(1, 180)

    # 查询
    def handleCalc(self):
        # 每次执行的时候先清空table的数据
        self.ui.table.clearContents()

        # 遍历结果
        i = self.ui.table.rowCount()
        if i != 0:
            row = i
            while row > 0:
                self.ui.table.removeRow(row - 1)
                row = row - 1

        result = self.search_data()

        if not result:
            QMessageBox().warning(self, '提示', '没有符合条件的记录')
            return

        # 解析我们要获取的内容
        infos = result['data']

        i = 0
        for info in infos:
            self.ui.table.insertRow(i)

            时间 = remove_tags(info['context'])
            物流状态 = remove_tags(info['time'])

            item = QTableWidgetItem('时间')
            item.setText(时间)
            self.ui.table.setItem(i, 1 , item)

            item = QTableWidgetItem('物流状态')
            item.setText(物流状态)
            self.ui.table.setItem(i, 0 , item)

            i = i + 1


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


    def search_data(self):
        base_url = 'https://www.kuaidi100.com/query?type=huitongkuaidi&postid={}&temp=0.18934088835993945&phone='

        num = self.ui.lineEdit.text()

        num = '550003287763556'

        # for i in range(1):
        url = base_url.format(num)
        response = requests.get(url)
        res_dict = json.loads(response.text)

        return res_dict


if __name__ == '__main__':
    app = QApplication()
    # 加载 icon
    app.setWindowIcon(QIcon('logo.png'))
    stats = Stats( )
    stats.ui.show()
    app.exec_()