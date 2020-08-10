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
        # self.ui = QUiLoader().load('Jd_Info.ui')
        self.ui = QUiLoader().load('../00_项目文件库/1_UI/Jd_Info.ui')
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
            QMessageBox().warning(self, '提示', '请先选择简历存放的文件夹')
            return


        self.ui.button1.setEnabled(False)
        FILE_DIR = file_path
        OUT_DIR = file_path + r"/resume-data.xlsx"

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

        df = pd.DataFrame()
        # os.listdir 方法表示列出该路径下的所有文件
        for folder in os.listdir(FILE_DIR):
            file_dir = os.path.join(os.path.abspath(FILE_DIR), folder)
            if os.path.isdir(file_dir):  # 遍历该路径下的所有,如果是文件夹，则继续遍历
                paths = find_files(file_dir)

                for index, file_path in enumerate(paths):
                    # print(f'index:{index},file_path:{file_path}')
                    info = Extractor(file_dir=file_path).search()
                    df = df.append(info,ignore_index=True)
                    text = ""
                    text = str(jd_index) + "   " + info["file_name"] +"   "+ info["user_name"]+"   " + info["phone"]+"   " + info["sex"]+"   " + info["age"]+"   " + info["degree"]+"   " + info["email"]
                    self.ui.text.append(text)
                    self.ui.text.append('------'*20)

                    QApplication.processEvents() #定时刷新
                    time.sleep(0.00001)
                    jd_index = jd_index + 1
                    jd_qty = jd_qty + 1

            elif os.path.isfile(file_dir): # 如果是文件，且格式是PDF的或者WORD的就直接读取
               if os.path.splitext(file_dir)[1] == '.pdf' or os.path.splitext(file_dir)[0] == '.docx':

                    info = Extractor(file_dir).search()

                    df = df.append(info, ignore_index=True)
                    text = ""
                    text = str(jd_index) + "   " + info["file_name"] + "   " + info["user_name"] + "   " + info[
                        "phone"] + "   " + info["sex"] + "   " + info["age"] + "   " + info["degree"] + "   " + info[
                               "email"]

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

        self.ui.text.append("所有简历已经处理完毕，总计： {} 份简历" .format(jd_qty))
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
        # elif os.path.splitext(self.file_dir)[1] == ".docx":
        #     doc = docx.Document(self.file_dir)
        #     for para in doc.paragraphs:
        #         text += para.text
        return text

    def __extract_words(self):
        """抽取单词"""
        words = []
        if os.path.splitext(self.file_dir)[1] == ".pdf":
            pdf = pb.open(self.file_dir)
            for page in pdf.pages:
                words += page.extract_words()
        # elif os.path.splitext(self.file_dir)[1] == ".docx":
        #     doc = docx.Document(self.file_dir)
        #     for para in doc.paragraphs:
        #         words.append(para.text)
        return words

    def __search_name(self):
        """搜索姓名"""
        names = []

        # 针对
        # 先通过"姓名"字段去查找”
        for line in full_text.split("\n"):
            if re.search(r"姓\s*名", line):
                name = re.findall(r"姓\s*名[:：\s]*[\u4e00-\u9fa5]{2,4}", line)[0]
                names.append(re.sub(r"[姓名:：\s]", "", name))

        # 在"姓名"字段中找不到结果，有些JD 有ID号，可以去查到姓名
        if len(names) < 1:
            for line in re.split(r"\n+", full_text):
                if re.search(r'(.*)(\s+)ID:',line):
                    names = re.search(r'(.*)(\s+)ID:',line)
                    if 2 <= len(names.group(1)) <= 4:
                        names = names.group(1)
                        break

        # 针对智联招聘的简历特殊处理
        if len(names) < 1  and '智联' in file_name:
            for line in re.split(r"\n+", full_text):
                if re.search(r'(招聘.+网)',line):
                    line = re.sub('\s+','',line)
                    line = re.sub('(招聘|网)','',line)
                    #去重
                    newname=''
                    for char in line:
                        if char not in newname:
                            newname+=char

                    names = newname
                    break

        # 在"姓名"字段中找不到结果，则按照文字长度去猜测一个
        if len(names) < 1:
            for line in re.split(r"\n|\s+", full_text):
                if re.search(r"\d", line):
                    continue
                word = ""
                for w in line:  # 去重
                    if w not in word:
                        word += w
                if 2 <= len(word) <= 4:
                    _names = re.findall(r"[\u4e00-\u9fa5]{2,4}", word)
                    names += _names
                    # break
        return names

    def __search_email(self):
        """搜索Email地址"""
        full_words = self.__extract_words()
        email = ""
        for word in full_words:
            if os.path.splitext(self.file_dir)[1] == ".pdf":
                text = word["text"]
            else:
                text = word
            if "@" in text and "." in text:
                for e in re.findall(r"[a-zA-Z0-9_\-.@]+", text):
                    if "@" in e:
                        email = e
                        break
            if email != "":
                break
        return email

    def __search_phone(self):
        """搜索电话号码"""
        # full_text = self.__extract_text()
        phone = ""
        # 直接通过文件名查找
        file_name = re.split(r"/+|\\+", self.file_dir)[-1]
        number = re.findall(r"\d{11,13}", file_name)
        if len(number) > 0 and re.search(r"^1", number[0]):
            phone = number[0]
        else:
            # 通过关键词查找
            for line in re.split(r"[\n\s]+", full_text):
                if "电话" in line or "手机" in line :

                    line = re.sub(r"[()（）：:+\-]", "", line)
                    number = re.findall(r"\d{11,13}", line)[0]
                    phone = re.sub(r"^(86)", "", number)
                    break
            # 直接通过数字长度查找
            if phone == "":
                text = re.sub(r"[()（）+\-]", "", full_text)
                phones = re.findall(r"\d{11,13}", text)
                phones = [re.sub(r"^(86)", "", p) for p in phones if re.search(r"^1", re.sub(r"^(86)", "", p))]
                phone = ",".join(set(phones))
        return phone

    def __search_age(self):
        """搜索年龄"""
        age = []
        # 先通过"岁关键字"字段去查找”
        for line in full_text.split("\n"):
            age1 = re.search(r'(.*)(\d.)(\s*岁)', line)
            if age1:
                if "智联" in file_name:
                    age1 = re.search(r'(.*\s+)(\d*)(岁岁.*)', line)
                    age = age1.group(2)
                    #去重
                    age = list(age)
                    age[0] = ''
                    age[2] = ''
                    age = ''.join(age)
                    break
                else:
                    age = age1.group(2)
                    break

        if age1 == None:
            for line in full_text.split("\n"):
                age1 = re.search(r'(\|)(\d{2})(\s*)', line)
                if age1:
                    age1 = age1.group(2)
                    if 20 <= int(age1) <= 50:
                        age = age1
                        break
        return age

    def __search_sex(self):
        # """搜索性别"""
        sex = []
        # 先通过"性别"字段去查找”
        for line in full_text.split("\n"):
            sex = re.search(r"[男女]", line)
            if sex:
                sex = sex.group(0)
                break

        return sex

    def __search_degree(self):
        # """搜索学历"""
        # 通过关键字段字段去查找”
        for line in full_text.split("\n"):
            degree = re.search(r'初中以下|高中|中技|中专|大专|本科|硕士|博士|MBA', line)
            if degree:
                degree = degree.group(0)
                break

        return degree

    def search(self):
        """入口函数，返回搜索结果"""
        global file_name

        sep_dir = re.split(r"/+|\\+", self.file_dir)
        directory = sep_dir[-2]
        file_name = sep_dir[-1]

        info = {"directory": directory,
                "file_name": file_name,
                "user_name": "",
                "phone": "",
                "sex": "",
                "age": "",
                "degree":"",
                "email": ""
                }

        global full_text

        full_text = self.__extract_text()
        # 查找姓名
        try:
            names = self.__search_name()
            info["user_name"] = "".join(names)
        except Exception as e:
            print(e)

        # 查找电话
        try:
            phone = self.__search_phone()
            info["phone"] = phone
        except Exception as e:
            print(e)

        # 查找Email
        try:
            email = self.__search_email()
            info["email"] = email
        except Exception as e:
            print(e)

        # 查找性别
        try:
            sex = self.__search_sex()
            info["sex"] = sex
        except Exception as e:
            print(e)

        # 查找年龄
        try:
            age = self.__search_age()
            info["age"] = age
        except Exception as e:
            print(e)

        # 查找学历
        try:
            degree = self.__search_degree()
            info["degree"] = degree
        except Exception as e:
            print(e)
        return info


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
        app.setWindowIcon(QIcon('../00_项目文件库/1_UI/logo.png'))
        stats = Stats()
        stats.ui.show()
        app.exec_()
        app.quit()
        app.kill()
        # sys.exit(app.exec_())
    except Exception as e:
        print(e)