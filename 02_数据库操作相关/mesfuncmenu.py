import json
import tkinter

import psycopg2


# 读取db配置  psycopg2 postgreSQL包
def read_json():
    db_info = {}
    with open('../00_项目文件库/2_File/mesdb.json', 'r') as load_f:  # 传入标识符'r'表示读取文件
        load_dict = json.load(load_f)
        db_info = load_dict
    conn = psycopg2.connect(database=db_info['database'], user=db_info['user'], password=db_info['password'],
                            host=db_info['host'], port=db_info['port'])
    return conn

# 查询
def get_mes_info(query_name, tk_result):
    text = f"--查询:{query_name} \n"
    if query_name == '':
        text += "查询条件为空 \n"
    else:
        db_conn = read_json()
        cur = db_conn.cursor()
        menu_sql = f"select a.view_id,a.name as name1,b.name as name2,COALESCE(c.name,'无') as name3," \
              f"COALESCE(d.name,'无') as name4,COALESCE(e.name,'无') as name5" \
              f" from sy_func a left join sy_func b on a.up_id=b.id left join sy_func c on b.up_id=c.id" \
              f" left join sy_func d on c.up_id=d.id left join sy_func e on d.up_id=e.id" \
              f" where a.name like'%{query_name}%' and a.type='1'"
        cur.execute(menu_sql)
        menu_results = cur.fetchall()
        if len(menu_results) == 0:
            text += f'查不到[{query_name}]菜单 \n'
            text += "\n"
        elif len(menu_results) > 5:
            text += '返回数据大于5条，请填写详细菜单名称 \n'
            text += "\n"
        else:
            for row in menu_results:
                view_id = row[0]
                text += f'菜单路径为:{row[5]}-{row[4]}-{row[3]}-{row[2]}-{row[1]} \n'
                view_sql = f"select a.view_name as name1,b.m_name as name2,COALESCE(c.m_name,'无') as name3," \
                           f"COALESCE(d.m_name,'无') as name4,COALESCE(e.m_name,'无') as name5" \
                           f" from ms_view_model a left join ms_buss_model b on a.mid=b.id " \
                           f"left join ms_buss_model c on b.up_m_id=c.id left join ms_buss_model d on c.up_m_id=d.id " \
                           f"left join ms_buss_model e on d.up_m_id=e.id " \
                           f"where a.id='{view_id}'"
                cur.execute(view_sql)
                view_result = cur.fetchall()[0]
                text += f'视图路径为:{view_result[4]}-{view_result[3]}-{view_result[2]}-{view_result[1]}-{view_result[0]} \n'
                text += "\n"
        db_conn.close()
    tk_result.insert(1.0, text)

# 清屏
def clear_text(tk_result):
    tk_result.delete('1.0','end')

    # 画界面
def create_tk():
    root = tkinter.Tk()     # 创建顶层窗口
    root.geometry('700x400')     # 初始化窗口大小
    root.title("查询菜单路径")   # 标题

    label_name = tkinter.Label(root, text='请输入要查询的菜单名称(支持模糊查询):', anchor='w')
    label_name.place(x=50, y=30, width=230, height=30)

    entry_name = tkinter.Entry(root, bd=1)
    entry_name.place(x=280, y=30, width=150, height=30)

    entry_result = tkinter.Text(root, bd=1)
    entry_result.place(x=50, y=90, width=600, height=250)

    # 回车触发查询事件
    entry_name.bind("<Return>", lambda event:get_mes_info(entry_name.get(), entry_result))

    button_query = tkinter.Button(root, text='查询', command=lambda: get_mes_info(entry_name.get(), entry_result))
    button_query.place(x=450, y=30, width=50, height=30)

    button_query = tkinter.Button(root, text='清屏', command=lambda: clear_text(entry_result))
    button_query.place(x=520, y=30, width=50, height=30)

    root.mainloop()

# 用于mes菜单查询和对应视图查询
if __name__ == '__main__':
    create_tk()