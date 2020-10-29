from tkinter import *
from requests import get, exceptions
import tkinter.messagebox
import clipboard
import tkinter.filedialog


class getmain:
    def __init__(self):
        self.root = Tk()
        self.root.title("网站爬取工具 - xiaosi4081")
        self.root.geometry("600x300")
        self.menu()
        self.maincode()
        self.root.mainloop()

    def getting(self, url):
        try:
            headers = [{
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"},
                       {
                           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}]
            for i in headers:
                res = get(url, headers=i).text
                if res != "":
                    break
            self.result.delete(0.0, END)
            self.result.insert(0.0, res)
        except exceptions.MissingSchema:
            tkinter.messagebox.showerror('错误', 'url有误')

    def copy(self):
        clipboard.copy(self.result.get(0.0, END))

    def savefile(self):
        path = tkinter.filedialog.asksaveasfile()
        path.write(str(self.result.get(0.0, END)))
        path.close()

    def closewindow(self):
        self.root.destroy()
        exit()

    def maincode(self):
        frame1 = LabelFrame(self.root, text="input")

        urllabel = Label(frame1, text="url is:   ")
        urllabel.pack()
        urllabel.grid(row=1, column=1)
        self.url = Entry(frame1)
        self.url.grid(row=1, column=2)
        startButton = Button(frame1, text="start", command=lambda: self.getting(self.url.get()))
        startButton.grid(row=1, column=3)
        frame1.pack()
        resultFrame = LabelFrame(self.root, text="result")
        self.result = Text(resultFrame, width=35, height=15)
        resultcopy = Button(resultFrame, text="复制到剪贴板", command=self.copy)
        self.result.pack()
        resultcopy.pack()
        resultFrame.pack()

    def menu(self):
        menubar = Menu(self.root)
        menu_a = Menu(self.root)
        for (key, value) in (("保存为", self.savefile), ("关闭窗口", self.closewindow)):
            menu_a.add_command(label=key, command=value)

        menubar.add_cascade(label='文件', menu=menu_a)
        self.root["menu"] = menubar


if __name__ == "__main__":
    bfi = getmain()