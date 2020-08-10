import pymysql

# pip install pymysql
def get_mysql_data():
    # 打开数据库连接
    db = pymysql.connect(host="ip", user="user",
                         password="password", db="cthdev", port=3306)
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    sql = "select * from cth_user"
    try:
        cur.execute(sql)    # 执行sql语句
        results = cur.fetchall()    # 获取查询的所有记录
        # 遍历结果
        for row in results:
            user_id = row[0]
            user_name = row[1]
            user_age = row[2]
            print(user_id, user_name, user_age)
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接


if __name__ == '__main__':
    get_mysql_data()