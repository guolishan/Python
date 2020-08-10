import tkinter

import pymysql


# 查询
def get_dpt_info(query_name, tk_result):
    text = f"--查询:{query_name} \n"
    if query_name == '':
        text += "查询条件为空 \n"
    else:
        # 打开数据库连接
        db = pymysql.connect(host="", user="root",password="Wb1!2@3#4$", db="h3bpm-online", port=3306)
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        sql = f"select b.name as '员工',a.name as '部门',c.name as '上级部门',IFNULL(d.name, '无') as '上两级部门',IFNULL(e.name, '无') as '上三级部门',IFNULL(f.name, '无') as '上四级部门' from ot_organizationunit a left join ot_user b on b.parentID=a.objectID left join ot_organizationunit c on c.ObjectID=a.ParentID left join ot_organizationunit d on d.ObjectID=c.ParentID left join ot_organizationunit e on e.ObjectID=d.ParentID left join ot_organizationunit f on f.ObjectID=e.ParentID where b.name like'%{query_name}%'"
        try:
            cur.execute(sql)    # 执行sql语句
            results = cur.fetchall()    # 获取查询的所有记录
            if len(results) > 20:
                text += "返回数据大于20条，请填写详细员工 \n"
            elif len(results) == 0:
                text += f"[{query_name}]查询不到 \n"
            else:
                # 遍历结果
                for row in results:
                    text += f"{row[0]}:{row[1]}-{row[2]}-{row[3]}-{row[4]}-{row[5]} \n"
        except Exception as e:
            raise e
        finally:
            db.close()  # 关闭连接
    text += "\n"
    tk_result.insert(1.0, text)

    print('test')


# 画界面
def create_tk():
    root = tkinter.Tk()     # 创建顶层窗口
    root.geometry('700x350')     # 初始化窗口大小
    root.title("查询员工部门")   # 标题

    label_name = tkinter.Label(root, text='请输入要查询的员工名(支持模糊查询):', anchor='w')
    label_name.place(x=50, y=30, width=210, height=30)

    entry_name = tkinter.Entry(root, bd=1)
    entry_name.place(x=260, y=30, width=150, height=30)

    entry_result = tkinter.Text(root, bd=1)
    entry_result.place(x=50, y=90, width=600, height=200)

    button_query = tkinter.Button(root, text='查询', command=lambda: get_dpt_info(entry_name.get(), entry_result))
    button_query.place(x=450, y=30, width=50, height=30)

    root.mainloop()


if __name__ == '__main__':
    create_tk()
