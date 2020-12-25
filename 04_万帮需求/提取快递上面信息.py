import os
import re
import sys
import time

import pandas as pd
import pdfplumber as pb
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from win32com.client import Dispatch

file_path = " "


class Stats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 从文件中加载UI定义
        self.ui = QUiLoader().load('Express_Info.ui')
        # self.ui = QUiLoader().load('../00_项目文件库/1_UI/Express_Info.ui')
        # 选取文件夹
        file_path = self.ui.button2.clicked.connect(self.handleCalc)
        #解析简历
        self.ui.button1.clicked.connect(self.handleJd)

    def handleCalc(self):
        global file_path
        file_path = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        self.ui.edit.setText(file_path)
        return file_path

    def handleJd(self):

        global file_path

        if not os.path.exists(file_path):
            QMessageBox().warning(self, '提示', '请先选择快递信息存放的文件夹')
            return


        self.ui.button1.setEnabled(False)
        FILE_DIR = file_path
        OUT_DIR = file_path + r"/express-data.xlsx"

        args = sys.argv


        if len(args) > 1:
            FILE_DIR = args[1]
        if len(args) > 2:
            OUT_DIR = args[2]
            FILE_DIR = args[1]

        # 文件存在，则追加序号
        cnt = 0
        while os.path.isfile(os.path.abspath(OUT_DIR)):
            OUT_DIR = os.path.splitext(OUT_DIR)[0] + "_" + str(cnt) + ".xlsx"
            cnt += 1

        writer = pd.ExcelWriter(OUT_DIR)


        # 图形界面中QTextBrowser控件框初始化
        self.ui.text.clear()
        # 有时，浏览框里面的内容长度超出了可见范围，我们在末尾添加了内容，往往希望控件自动翻滚到当前添加的这行，可以通过 ensureCursorVisible 方法来实现
        self.ui.text.ensureCursorVisible()


        self.cursor = self.ui.text.textCursor()
        self.ui.text.moveCursor(self.cursor.End)

        s_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.ui.text.append("程序开始执行：{}".format(s_time))
        self.ui.text.append('------' * 20)

        global jd_qty,jd_index
        jd_index = 0
        jd_qty = 0.

        global  df

        df = pd.DataFrame()
        # os.listdir 方法表示列出该路径下的所有文件
        for folder in os.listdir(FILE_DIR):
            file_dir = os.path.join(os.path.abspath(FILE_DIR), folder)
            if os.path.isdir(file_dir):  # 遍历该路径下的所有,如果是文件夹，则继续遍历
                paths = find_files(file_dir)

                for index, file_path in enumerate(paths):
                    file_name = Extractor(file_dir=file_path).search()
                    text = ""
                    text = file_name + "处理完毕！"

                    self.ui.text.append(text)
                    self.ui.text.append('------'*20)

                    QApplication.processEvents() #定时刷新
                    time.sleep(0.00001)
                    jd_index = jd_index + 1
                    jd_qty = jd_qty + 1

            elif os.path.isfile(file_dir): # 如果是文件，且格式是PDF的或者WORD的就直接读取
               if os.path.splitext(file_dir)[1] == '.pdf' or os.path.splitext(file_dir)[0] == '.docx':

                   file_name = Extractor(file_dir).search()

                   text = ""
                   text = file_name + "处理完毕！"

                   self.ui.text.append(text)
                   self.ui.text.append('------' * 20)

                   QApplication.processEvents()  # 定时刷新
                   time.sleep(0.000001)
                   jd_index = jd_index + 1
                   jd_qty = jd_qty + 1
            else:
                print('该路径下文件为空')

        if len(os.listdir(FILE_DIR)) < 1:
            QMessageBox().warning(self, '提示', '该路径下文件为空')
            return

        df.to_excel(writer)

        QApplication.processEvents()  # 定时刷新
        time.sleep(0.000001)

        self.ui.text.append("所有快递已经处理完毕，总计： {} 份快递" .format(jd_qty))
        self.ui.text.append("文件已经保存文件到:{} ".format( OUT_DIR))
        self.ui.text.append('------'*20)

        writer.save()

        QApplication.processEvents()  # 定时刷新
        time.sleep(0.000001)

        e_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.ui.text.append("程序结束执行：{}".format(e_time))
        self.ui.button1.setEnabled(True)


class Extractor(object):
    """抽取单个文件的信息"""
    def __init__(self, file_dir):
        self.file_dir = file_dir
        if os.path.splitext(self.file_dir)[1] in [".doc", ".docx"]:
            try:
                self.__word2pdf()
            except Exception as e:
                print(e)
                return

    def __doc2docx(self):
        """doc转为docx"""
        w = Dispatch('Word.Application')
        w.Visible = 0
        w.DisplayAlerts = 0
        doc = w.Documents.Open(self.file_dir)
        new_path = os.path.splitext(self.file_dir)[0] + '.docx'
        doc.SaveAs(new_path, 12, False, "", True, "", False, False, False, False)
        doc.Close()
        w.Quit()
        os.remove(self.file_dir)
        self.file_dir = new_path
        return new_path

    def __word2pdf(self):
        """word转为pdf"""
        w = Dispatch('Word.Application')
        w.Visible = 0
        w.DisplayAlerts = 0
        doc = w.Documents.Open(self.file_dir)
        new_path = os.path.splitext(self.file_dir)[0] + '.pdf'
        doc.SaveAs(new_path, FileFormat=17)
        doc.Close()
        w.Quit()
        os.remove(self.file_dir)
        self.file_dir = new_path
        return new_path


    def __extract_text(self):
        """抽取文本内容"""
        text = ""
        if os.path.splitext(self.file_dir)[1] == ".pdf":
            pdf = pb.open(self.file_dir)
            for page in pdf.pages:
                text += page.extract_text() if page.extract_text() else ""
        return text


    def __extract_words(self):
        """抽取单词"""
        words = []
        if os.path.splitext(self.file_dir)[1] == ".pdf":
            pdf = pb.open(self.file_dir)
            for page in pdf.pages:
                words += page.extract_words()
        return words


    def __search_number(self):
        global file_name

        # print(file_name)
        # print(full_text)

        """搜索快递单号"""
        number = []
        i = 1
        for line in full_text.split("\n"):
            if file_name.find('yz') != -1:
                if i == 5:
                    number = line.replace(" ", "")
                    break
            else:
                if i == 4:
                    number = line
                    break
            i = i + 1

        return number

    def __search_address(self):
        """搜索快递收货地址"""
        address_t = []
        i = 1

        for line in full_text.split("\n"):
            if line[0] == '寄':
                break

            if file_name.find('yz') != -1:
                line = line.replace(" ", "")
                if i >= 15:
                    if i == 15:
                        line = line[:-1]  #去除字符串最后一个字符

                    if len(line) == 1:
                        line = ''

                    address = line
                    address.replace(" ", "")
                    address_t.append(address)
            else:
                if i >= 7:
                    address = line
                    address_t.append(address)

            i = i + 1

        return address_t

    def search(self):
        """入口函数，返回搜索结果"""
        global file_name,df

        sep_dir = re.split(r"/+|\\+", self.file_dir)
        directory = sep_dir[-2]
        file_name = sep_dir[-1]

        info = {"directory": directory,
                "file_name": file_name,
                "exp_nubmer": "",
                "exp_address": "",
                }

        global full_text

        if os.path.splitext(self.file_dir)[1] == ".pdf":
            pdf = pb.open(self.file_dir)
            for page in pdf.pages:
                full_text = page.extract_text() if page.extract_text() else ""
                # 查找快递单号
                try:
                    exp_nubmer = self.__search_number()
                    info["exp_nubmer"] = "".join(exp_nubmer)
                except Exception as e:
                    print(e)

                # 查找寄件地址
                try:
                    exp_address = self.__search_address()
                    info["exp_address"] = "".join(exp_address)
                except Exception as e:
                    print(e)

                df = df.append(info, ignore_index=True)

        return file_name


def find_files(file_dir):
    """迭代查找文件"""
    file_paths = []
    for root, _, files in os.walk(file_dir):
        for file in files:
            path = os.path.join(root, file)
            rear = os.path.splitext(path)[1]
            if rear in [".doc", ".docx", ".pdf"]:
                file_paths.append(path)
    return file_paths

if __name__ == '__main__':
    try:
        app = QApplication([])
        # 加载 icon
        # app.setWindowIcon(QIcon('../00_项目文件库/1_UI/logo.png'))
        app.setWindowIcon(QIcon('logo.png'))
        stats = Stats()
        stats.ui.show()
        app.exec_()
        app.quit()
        app.kill()
        # sys.exit(app.exec_())
    except Exception as e:
        print(e)