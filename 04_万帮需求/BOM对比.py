import pandas as pd
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *


global bom_version1,bom_version2,index_a,index_b,df_a,df_b,i

index_a = 0
index_b = 0
i = 0

class Stats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 从文件中加载UI定义
        # self.ui = QUiLoader().load('BOM_Compare.ui')
        self.ui = QUiLoader().load('../00_项目文件库/1_UI/BOM_Compare.ui')

        # 初始化table控件
        self.init_ui()

        # 按钮事件
        self.ui.button.clicked.connect(self.handleCalc)

    def init_ui(self):
        self.ui.tab.setCurrentIndex(0)  # 设定当前显示的Tab页

        # Tab(所有页面)属性设定
        # ---------------------------------------------------------------------------
        # 设定第1列的宽度为 180像素
        self.ui.table1.setRowCount(4)  # 设定行
        self.ui.table1.setColumnCount(9)  # 设定列

        self.ui.table1.setColumnWidth(0, 180)
        # 设定第2列的宽度为 100像素
        self.ui.table2.setColumnWidth(1, 180)

        self.ui.table1.horizontalHeader().setStretchLastSection(True)

        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        self.ui.table1.setHorizontalHeaderLabels(
            ['BOM版本', '父项物料编码', '物料名称','项次','子项物料编码', '子项物料名称', '子项单位', '用量:分子', '用量:分母'])


        # Tab(差异行数据)属性设定
        # --------------------------------------------------------------------------------
        # 设定第1列的宽度为 180像素
        self.ui.table2.setRowCount(4)  # 设定行
        self.ui.table2.setColumnCount(9)  # 设定列

        self.ui.table2.setColumnWidth(0, 180)
        # 设定第2列的宽度为 100像素
        self.ui.table2.setColumnWidth(1, 180)

        self.ui.table2.horizontalHeader().setStretchLastSection(True)

        # 设置水平方向的表头标签与垂直方向上的表头标签，注意必须在初始化行列之后进行，否则，没有效果
        self.ui.table2.setHorizontalHeaderLabels(
            ['BOM版本', '父项物料编码', '物料名称','项次','子项物料编码', '子项物料名称', '子项单位', '用量:分子', '用量:分母'])


    def handleCalc(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择你要上传的Excel文件",  # 标题
            r"C:\\Users\\dell\\Desktop\\",  # 起始目录
            "文件类型 (*.xls *.xlsx)"  # 选择类型过滤项，过滤内容在括号中
        )


        self.ui.Edit.setText(file_path)

        # 读取文件
        df_raw = pd.read_excel(file_path, header=0)

        # 筛选其中的某些类，产生新的Data Frame
        df_new = pd.DataFrame(df_raw,columns=['BOM版本','父项物料编码','物料名称','项次', '子项物料编码', '子项物料名称', '子项规格型号', '子项单位',  '用量:分子', '用量:分母'])

        global bom_version1,bom_version2,index_a,index_b,df_a,df_b

        df_a = pd.DataFrame(columns=['BOM版本','父项物料编码','物料名称','项次', '子项物料编码', '子项物料名称', '子项规格型号', '子项单位',  '用量:分子', '用量:分母'])
        df_b = pd.DataFrame(columns=['BOM版本','父项物料编码','物料名称','项次', '子项物料编码', '子项物料名称', '子项规格型号', '子项单位',  '用量:分子', '用量:分母'])
        # 针对空格进行数据填充
        df_new = df_new.fillna(method='pad',axis=0)

        # 当用行号索引的时候, 尽量用 iloc 来进行索引; 而用标签索引的时候用 loc, ix 尽量别用
        data = df_new.loc[:,['BOM版本']].drop_duplicates().dropna()

        global bom_version1,bom_version2
        bom_version1 = data.iloc[0,0]
        bom_version2 = data.iloc[1,0]

        self.ui.lineEdit_2.setText(bom_version1)
        self.ui.lineEdit_3.setText(bom_version2)

        def split_table(series):  # 根据BOM版本拆分成俩个不同的Data Frame
            global bom_version1,bom_version2,index_a,index_b,df_a,df_b

            bom_version = series['BOM版本']

            if bom_version == bom_version1:
                df_a.loc[index_a] = series
                # 增加一列tmp,作为辅助列
                df_a.loc[index_a,'tmp'] = ''.join([str(series['子项物料编码']),str(series['子项单位']),str(series['用量:分子']),str(series['用量:分母'])])
                index_a = index_a + 1
            elif bom_version == bom_version2:
                df_b.loc[index_b] = series
                df_b.loc[index_b,'tmp'] = ''.join([str(series['子项物料编码']),str(series['子项单位']),str(series['用量:分子']),str(series['用量:分母'])])


        # 将不同版本的数据存放到不同的Data Frame
        df_new.apply(split_table,axis=1)

        #实现Vlookup功能
        if len(df_a) >= len(df_b):
            # 行标签重名对于merge是不会有影响的，这里将表2的项次和子项物料编码重名的目的是为了将数据output到table上不受影响
            df_b.rename(columns={'项次':'项次_N'},inplace=True)
            df_b.rename(columns={'子项物料编码':'子项物料编码_N'},inplace=True)
            result = pd.merge(df_a,df_b.loc[:,['tmp','项次_N','子项物料编码_N']],how='left',on = 'tmp')
        else:
            df_a.rename(columns={'项次':'项次_N'},inplace=True)
            df_a.rename(columns={'子项物料编码':'子项物料编码_N'},inplace=True)
            result = pd.merge(df_b,df_a.loc[:,['tmp','项次_N','子项物料编码_N']],how='left',on = 'tmp')


        # 数据输出到Tab页签的table

        # 每次执行的时候先清空table的数据
        self.ui.table1.clearContents()

        # 先清除table的多余行
        i = self.ui.table1.rowCount()
        if i != 0:
            row = i
            while row > 0:
                self.ui.table1.removeRow(row - 1)
                row = row - 1

        # 数据处理函数
        def output_data(series):
            global  i
            self.ui.table1.insertRow(i)

            item = QTableWidgetItem('BOM版本')
            item.setText(series['BOM版本'])
            self.ui.table1.setItem(i, 0 , item)

            item = QTableWidgetItem('父项物料编码')
            item.setText(series['父项物料编码'])
            self.ui.table1.setItem(i, 1 , item)

            item = QTableWidgetItem('物料名称')
            item.setText(series['物料名称'])
            self.ui.table1.setItem(i, 2 , item)

            item = QTableWidgetItem('项次')
            item.setText(str(series['项次']))
            self.ui.table1.setItem(i, 3 , item)

            item = QTableWidgetItem('子项物料编码')
            item.setText(str(series['子项物料编码']))
            self.ui.table1.setItem(i, 4 , item)

            item = QTableWidgetItem('子项物料名称')
            item.setText(series['子项物料名称'])
            self.ui.table1.setItem(i, 5 , item)

            item = QTableWidgetItem('子项单位')
            item.setText(series['子项单位'])
            self.ui.table1.setItem(i, 6 , item)

            item = QTableWidgetItem('用量:分子')
            item.setText(str(series['用量:分子']))
            self.ui.table1.setItem(i, 7 , item)

            item = QTableWidgetItem('用量:分母')
            item.setText(str(series['用量:分母']))
            self.ui.table1.setItem(i, 8 , item)

            self.ui.table2.insertRow(i)

            item = QTableWidgetItem('BOM版本')
            item.setText(series['BOM版本'])
            self.ui.table2.setItem(i, 0 , item)

            item = QTableWidgetItem('父项物料编码')
            item.setText(series['父项物料编码'])
            self.ui.table2.setItem(i, 1 , item)

            item = QTableWidgetItem('物料名称')
            item.setText(series['物料名称'])
            self.ui.table2.setItem(i, 2 , item)

            item = QTableWidgetItem('项次')
            item.setText(str(series['项次']))
            self.ui.table2.setItem(i, 3 , item)

            item = QTableWidgetItem('子项物料编码')
            item.setText(str(series['子项物料编码']))
            self.ui.table2.setItem(i, 4 , item)

            item = QTableWidgetItem('子项物料名称')
            item.setText(series['子项物料名称'])
            self.ui.table2.setItem(i, 5 , item)

            item = QTableWidgetItem('子项单位')
            item.setText(series['子项单位'])
            self.ui.table2.setItem(i, 6 , item)

            item = QTableWidgetItem('用量:分子')
            item.setText(str(series['用量:分子']))
            self.ui.table2.setItem(i, 7 , item)

            item = QTableWidgetItem('用量:分母')
            item.setText(str(series['用量:分母']))
            self.ui.table2.setItem(i, 8 , item)

            i = i + 1

        # 将不同版本的数据存放到不同的Data Frame
        result.apply(output_data,axis=1)

if __name__ == '__main__':
    app = QApplication([])
    # 加载 icon
    app.setWindowIcon(QIcon('../00_项目文件库/1_UI/logo.png'))
    stats = Stats()
    stats.ui.show()
    app.exec_()