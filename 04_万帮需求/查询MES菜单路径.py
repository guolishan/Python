import psycopg2
import xlwt
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QMessageBox
from PySide2.QtWidgets import QTableWidgetItem, QFileDialog


class Stats(QWidget):
    def __init__(self, parent=None):
        # super().__init__(parent)
        super(Stats, self).__init__(parent)

        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('../00_项目文件库/1_UI/Search_Menu.ui')
        #
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

        result = self.conn_db()

        if not result:
            QMessageBox().warning(self, '提示', '没有符合条件的记录')
            return

        i = 0
        for row in result:
            self.ui.table.insertRow(i)
            view_name = row[0]
            form_name = row[1]
            item = QTableWidgetItem('View_Name')
            item.setText(view_name)
            self.ui.table.setItem(i, 0 , item)

            item = QTableWidgetItem('Form_Name')
            item.setText(form_name)
            self.ui.table.setItem(i, 1 , item)

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


    def conn_db(self):
        # psycopg2 postgreSQL包
        conn = psycopg2.connect(database="n2db",user="n2admin",password="fefdee",
                                host="172.16.1.19",port="5432")
        cur = conn.cursor()
        input_var = self.ui.lineEdit.text()
        sql = f"SELECT a.view_name, c.form_name " \
              f"FROM ms_view_model a INNER JOIN ms_view_form_rel b ON a.id = b.viewid INNER JOIN ms_form_model c ON b.formid = c.id " \
              f"WHERE a.view_name LIKE '%{input_var}%';"

        cur.execute(sql)
        results = cur.fetchall()
        conn.close()
        return results

if __name__ == '__main__':
    app = QApplication()
    # 加载 icon
    app.setWindowIcon(QIcon('../00_项目文件库/1_UI/logo.png'))
    stats = Stats( )
    stats.ui.show()
    app.exec_()