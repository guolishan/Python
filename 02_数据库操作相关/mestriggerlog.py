import datetime
import json
import tkinter

import psycopg2


# 读取db配置
def read_json():
    db_info = {}
    with open('../00_项目文件库/2_File/mesdb.json', 'r') as load_f:  # 传入标识符'r'表示读取文件
        load_dict = json.load(load_f)
        db_info = load_dict
    conn = psycopg2.connect(database=db_info['database'], user=db_info['user'], password=db_info['password'],
                            host=db_info['host'], port=db_info['port'])
    return conn

# 查询异常
def get_info(tk_result, time_type):
    db_conn = read_json()
    cur = db_conn.cursor()
    if time_type == 0:
        # 获取当天零点
        date_str = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
    else:
        # 前N个小时
        date_str = (datetime.datetime.now() - datetime.timedelta(hours=fixed_num)).strftime("%Y-%m-%d %H:%M:%S")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"------{now_str} \n"
    try:
        query_sql1 = f"select b.trigger_name,a.trigger_id from ms_trigger_log a left join ms_trigger_model b on a.trigger_id=b.id where a.log_level='0' and to_char(a.create_date,'yyyy-MM-dd hh24:mi:ss') >= '{date_str}' group by b.trigger_name,a.trigger_id"
        cur.execute(query_sql1)    # 执行sql语句
        results = cur.fetchall()    # 获取查询的所有记录
        if len(results) == 0:
            text += f" 未发生异常 \n"
        else:
            text += f" 异常触发器为: \n"
            # 遍历结果
            for row in results:
                query_sql2 = f"select a.create_date from ms_trigger_log a where a.log_level='0' and to_char(a.create_date,'yyyy-MM-dd hh24:mi:ss') >= '{date_str}' and a.trigger_id='{row[1]}' order by a.create_date desc limit 1"
                cur.execute(query_sql2)    # 执行sql语句
                result = cur.fetchone()    # 获取查询的第一条记录
                text += f"--{row[0]}--最新异常时间:{result[0]} \n"
    except Exception as e:
        raise e
    finally:
        db_conn.close()  # 关闭连接
    text += "\n"
    tk_result.insert(1.0, text)

# 清屏
def clear_text(tk_result):
    tk_result.delete('1.0','end')


# 画界面
def create_tk():
    root = tkinter.Tk()     # 创建顶层窗口
    root.geometry('700x350')     # 初始化窗口大小
    root.title("触发器异常监控器")   # 标题

    label_name = tkinter.Label(root, text=f'每{fixed_num}小时自动查询一次', anchor='w')
    label_name.place(x=50, y=30, width=230, height=30)

    entry_result = tkinter.Text(root, bd=1)
    entry_result.place(x=50, y=90, width=600, height=200)

    button_query = tkinter.Button(root, text='手动查询当天异常', command=lambda: get_info(entry_result, 0))
    button_query.place(x=250, y=30, width=120, height=30)

    button_query = tkinter.Button(root, text='清屏', command=lambda: clear_text(entry_result))
    button_query.place(x=400, y=30, width=50, height=30)

    # 定时器
    def timer():
        get_info(entry_result, 1)
        root.after(fixed_base * fixed_num, timer)
    root.after(0, timer)

    root.mainloop()


# mes触发器异常监控器
if __name__ == '__main__':
    # 基数
    fixed_base = 1000 * 60 * 60
    # 小时数
    fixed_num = 1
    create_tk()
