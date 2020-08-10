import pymssql
from DBUtils.PooledDB import PooledDB


# 连接池 游标
def cur_database(db_name):
    if db_name == 'mssql':
        mssql_pool = PooledDB(creator=pymssql, mincached=2, maxcached=5, maxshared=3, maxconnections=6,
                        blocking=True, host='', user='sa', password='Wb1!2@3#4$',
                        database='demo', charset='utf8')
        return mssql_pool.connection().cursor()
    else:
        mysql_pool = PooledDB(creator=pymssql, mincached=2, maxcached=5, maxshared=3, maxconnections=6,
                        blocking=True, host='', user='sa', password='Wb1!2@3#4$', port=3306,
                        database='demo', charset='utf8')
        return mysql_pool.connection().cursor()

if __name__ == '__main__':
    db_name = 'mssql'
    cursor = cur_database(db_name)
    sql = "select count(1) from userInfo where username like '%cth%'" if db_name =='mssql' else ""
    cursor.excute(sql)
    row = cursor.fetchone()  # 取第一个
    print(row[0])