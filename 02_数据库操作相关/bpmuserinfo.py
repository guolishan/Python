import pymysql


def get_dpt_info(query_name):
    # 打开数据库连接
    db = pymysql.connect(host="", user="root",password="Wb1!2@3#4$", db="h3bpm-online", port=3306)
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    sql = f"select b.name as '员工',a.name as '部门',c.name as '上级部门',IFNULL(d.name, '无') as '上两级部门',IFNULL(e.name, '无') as '上三级部门',IFNULL(f.name, '无') as '上四级部门' from ot_organizationunit a left join ot_user b on b.parentID=a.objectID left join ot_organizationunit c on c.ObjectID=a.ParentID left join ot_organizationunit d on d.ObjectID=c.ParentID left join ot_organizationunit e on e.ObjectID=d.ParentID left join ot_organizationunit f on f.ObjectID=e.ParentID where b.name like'%{query_name}%'"
    try:
        cur.execute(sql)    # 执行sql语句
        results = cur.fetchall()    # 获取查询的所有记录
        if len(results) > 20:
            print("返回数据大于20条，请填写详细员工")
        elif len(results) == 0:
            print(f"[{query_name}]查询不到")
        else:
            # 遍历结果
            for row in results:
                print(f"{row[0]}:{row[1]}-{row[2]}-{row[3]}-{row[4]}-{row[5]}")
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


if __name__ == '__main__':
    for i in range(0, 10):
        input_name = input('请输入要查询的员工名(输入end结束):')
        if input_name == 'end':
            print("查询结束")
            break
        else:
            get_dpt_info(input_name)
