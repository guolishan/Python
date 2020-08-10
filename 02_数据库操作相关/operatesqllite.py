import random
import sqlite3


# 创建表
def create_table():
    conn = sqlite3.Connection('F:\cth\cth_py\lunch.db')
    print("Opened database success")
    cur = conn.cursor()
    q_sql = "select count(1) from sqlite_master where type='table' and name = 'lunch_menu'"
    c_sql = "create table lunch_menu (id integer primary key autoincrement,name varchar(30) not null,money varchar(30) not null,type varchar(10) not null,taste varchar(30) not null,state varchar(10) not null,create_time date)"
    cur.execute(q_sql)
    result = cur.fetchone()
    if result[0] == 0:
        cur.execute(c_sql)
        print("create success")
    else:
        print("table already exists")
    conn.commit()
    conn.close()


def random_choose():
    conn = sqlite3.Connection('F:\cth\cth_py\lunch.db')
    cur = conn.cursor()
    q_sql = "select a.* from lunch_menu a;"
    cur.execute(q_sql)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    rdm_results = random.sample(result,3)
    money = 0
    tips = ''
    for tup in rdm_results:
        money += int(tup[2])
        tip = f"{tup[4]}的{tup[1]}[{tup[3]}],"
        tips += tip
    print(tips)
    print(money)
    print(f"今天吃：{tips}总共{money}元")


if __name__ == '__main__':
    create_table()
    random_choose()