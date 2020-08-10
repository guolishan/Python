import cx_Oracle


# pip install cx_Oracle, 配置oracle instantclient的环境变量 https://www.cnblogs.com/eoalfj/p/10590604.html
def get_oracle_data(sql):
    # 打开数据库连接
    # db = cx_Oracle.connect('crmdev/crmdev@ip:1521/orcl')
    db = cx_Oracle.connect('czzhd/czzhd@ip:1521/orcl')
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    # sql = "select * from t_menu"
    try:
        print(sql)
        cur.execute(sql)    # 执行sql语句
        results = cur.fetchall()    # 获取查询的所有记录
        print(type(results))
        # 遍历结果
        for row in results:
            print(row)
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接
    return results