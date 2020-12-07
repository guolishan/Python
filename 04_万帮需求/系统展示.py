from tkinter import*
import webbrowser

# 第1步，实例化object，建立窗口window
window = Tk()

# 第2步，给窗口的可视化起名字
window.title('电动汽车智能充电系统绿色设计平台')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('400x300')  # 这里的乘是小x

def hit_mes():
    url = 'http://mes.wbtz.com/mc/fp/FpAction_forFpLogin.ms'
    webbrowser.open(url, new=0, autoraise=True)


def hit_rdm():
    url = 'https://rdm.wbtz.cloud/'
    webbrowser.open(url, new=0, autoraise=True)

def hit_plm():
    url = 'http://plmserver.wbtz.cloud.com:8888/Windchill/'
    webbrowser.open(url, new=0, autoraise=True)

def hit_k3c():
    url = 'https://k3c.wbtz.cloud/k3cloud/html5/index.aspx'
    webbrowser.open(url, new=0, autoraise=True)

def hit_bpm():
    url = 'http://bpm.wbtz.cloud/Portal/#/platform/loginhttp://bpm.wbtz.cloud/Portal/#/platform/login'
    webbrowser.open(url, new=0, autoraise=True)

def hit_hr():
    url = 'http://hr.wbtz.cloud/RedseaPlatform/'
    webbrowser.open(url, new=0, autoraise=True)

def hit_bi():
    url = 'http://172.16.3.8:8888/WebReport/ReportServer?op=fs'
    webbrowser.open(url, new=0, autoraise=True)

def hit_crm():
    url = 'https://www.fxiaoke.com/pc-login/build/login.html#crm/index'
    webbrowser.open(url, new=0, autoraise=True)

def hit_alm():
    url = 'https://wbusercenter.wbtz.cloud/login.do?callback=http://almgate.wbtz.cloud/oauth/login'
    webbrowser.open(url, new=0, autoraise=True)

#创建两个按钮
b1=Button(window, text='MES', relief='raised', width=8, height=2, command=hit_mes)
b1.grid(row=0, column=0, sticky=W, padx=5,pady=5)

b2=Button(window, text='ALM', font=('Helvetica 10 bold'),width=8, height=2,command=hit_alm)
b2.grid(row=0, column=1, sticky=W, padx=5, pady=5)

b3=Button(window, text='CRM', font=('Helvetica 10 bold'),width=8, height=2,command=hit_crm)
b3.grid(row=0, column=2, sticky=W, padx=5, pady=5)

b4=Button(window, text='K3C', font=('Helvetica 10 bold'),width=8, height=2,command=hit_k3c)
b4.grid(row=1, column=0, sticky=W, padx=5, pady=5)

b5=Button(window, text='BPM', font=('Helvetica 10 bold'),width=8, height=2,command=hit_bpm)
b5.grid(row=1, column=1, sticky=W, padx=5, pady=5)

b6=Button(window, text='PLM', font=('Helvetica 10 bold'),width=8, height=2,command=hit_plm)
b6.grid(row=1, column=2, sticky=W, padx=5, pady=5)

b7=Button(window, text='RDM', font=('Helvetica 10 bold'),width=8, height=2,command=hit_rdm)
b7.grid(row=2, column=0, sticky=W, padx=5, pady=5)

b8=Button(window, text='HR', font=('Helvetica 10 bold'),width=8, height=2,command=hit_hr)
b8.grid(row=2, column=1, sticky=W, padx=5, pady=5)

b9=Button(window, text='BI', font=('Helvetica 10 bold'),width=8, height=2,command=hit_bi)
b9.grid(row=2, column=2, sticky=W, padx=5, pady=5)

# 第6步，主窗口循环显示
window.mainloop()