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


# 修改标志
def get_info(bill_no, tk_result, wms_type):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"--------------{now_str}-------------- \n"
    if bill_no == '':
        text += f" 采购订单单号为空，请输入 \n"
    else:
        db_conn = read_json()
        cur = db_conn.cursor()
        try:
            count_sql = f"select count(*) from T_WMS_PO_DETAIL a where a.wpd_po ='{bill_no}'"
            cur.execute(count_sql)    # 执行sql语句
            count_result = cur.fetchone()    # 获取查询的记录
            if count_result[0] == 0:
                text += f" 采购订单未同步到mes，请在 物流中心-采购管理 手动同步单据 \n"
            else:
                # 上传二级
                query_sql = f"select count(*) from T_WMS_PO_DETAIL where outer_box_upload_flag='N' and wpd_po ='{bill_no}'"
                update_sql = f"update T_WMS_PO_DETAIL set outer_box_upload_flag='N' where wpd_po ='{bill_no}'"
                if wms_type == 1: # 上传三级
                    query_sql = f"select count(*) from T_WMS_PO_DETAIL where wpd_upload_flag='N' and wpd_po ='{bill_no}'"
                    update_sql = f"update T_WMS_PO_DETAIL set wpd_upload_flag='N' where wpd_po ='{bill_no}'"
                cur.execute(query_sql)    # 执行sql语句
                query_result = cur.fetchone()    # 获取查询的记录
                if query_result[0] != 0:
                    text += f" 请勿重复修改，请等待定时器同步 \n"
                else:
                    cur.execute(update_sql)    # 执行sql语句
                    db_conn.commit()
                    text += f" 修改成功，请等待定时器同步 \n"
        except Exception as e:
            db_conn.rollback()
            raise e
        finally:
            db_conn.close()  # 关闭连接
    text += "\n"
    tk_result.insert(1.0, text)


# 画界面
def create_tk():
    root = tkinter.Tk()     # 创建顶层窗口
    root.geometry('700x350')     # 初始化窗口大小
    root.title("云标签上传工具")   # 标题

    label_name1 = tkinter.Label(root, text='采购订单单号:', anchor='w')
    label_name1.place(x=50, y=30, width=100, height=30)

    mes_content = '1.k3c未同步mes的情况，请在 物流中心-采购管理 手动同步单据，然后修改对应标签任务状态\n' \
                  '2.mes有单据但是云标签没有的情况，请修改对应标签任务状态，然后等待定时器同步\n'

    label_name2 = tkinter.Label(root, text=mes_content, anchor='w', justify=tkinter.LEFT, fg='red') # 靠左
    label_name2.place(x=50, y=280, width=600, height=60)

    # 输入框
    entry_result1 = tkinter.Entry(root, bd=1)
    entry_result1.place(x=170, y=30, width=120, height=30)

    # 结果框
    entry_result2 = tkinter.Text(root, bd=1)
    entry_result2.place(x=50, y=70, width=600, height=200)

    button_query1 = tkinter.Button(root, text='上传二级（外箱物料）', command=lambda: get_info(entry_result1.get(), entry_result2, 0))
    button_query1.place(x=310, y=30, width=130, height=30)

    button_query2 = tkinter.Button(root, text='上传三级（物料）', command=lambda: get_info(entry_result1.get(), entry_result2, 1))
    button_query2.place(x=460, y=30, width=110, height=30)

    root.mainloop()


# mes触发器异常监控器
if __name__ == '__main__':
    create_tk()