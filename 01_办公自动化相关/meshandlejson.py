import json

import psycopg2


# 连接db
def db_connect():
    return psycopg2.connect(database='n2db', user='n2admin', password='***',
                            host='ip', port='9999')
# 处理数据
def update_mes():
    with open(json_path,'r',encoding='UTF-8') as load_f:  # 传入标识符'r'表示读取文件
        load_json = json.load(load_f)
    print(f'需要处理{len(load_json)}条数据')
    update_sql = ''
    for tmp_data in load_json:
        tmp_fid = tmp_data[0]
        tmp_bill_no = tmp_data[1]
        tmp_entry_id = tmp_data[2]
        update_sql = update_sql + f"update T_WMS_RECEIVE_ITEM set fsfjj=1 where fid='{tmp_fid}' and wri_doc_num='{tmp_bill_no}' " \
                                  f"and fentryid ='{tmp_entry_id}';"
    print(update_sql)
    cur = db_conn.cursor()
    try:
        cur.execute(update_sql)    # 执行sql语句
        db_conn.commit()
    except Exception as e:
        db_conn.rollback()
        raise e
    finally:
        db_conn.close()  # 关闭连接
    print('结束...')


# 读取json修改数据
if __name__ == '__main__':
    json_path='F:\cth\mes\k3c接口\k3c数据\k3c.json'
    db_conn = db_connect()
    update_mes()