import json

import pymssql

if __name__ == '__main__':
    with open('k3cdb.json','r',encoding='utf-8') as load_f:  # 传入标识符'r'表示读取文件
        load_dict = json.load(load_f)
    db_list = load_dict['db_list']
    update_url = load_dict['update_url']
    for db_config in db_list:
        db_name = db_config["name"]
        print(f"开始连接[{db_name}]...")
        # noinspection PyBroadException
        try:
            db_conn = pymssql.connect(database=db_config['database'], user=db_config['user'],
                                      password=db_config['password'], host=db_config['host'],
                                      port=db_config['port'])
            db_cur = db_conn.cursor()
            db_cur.execute("select c_url from t_wb_star_config where c_type=1")
            result = db_cur.fetchone()
            if result[0] == update_url:
                print("配置相同，不需要修改... \n")
                continue
            db_cur.execute(f"update t_wb_star_config set c_url = '{update_url}' where c_type=1")
            db_conn.commit()
            db_conn.close()
            print(f"成功更新[{db_name}][{db_cur.rowcount}]条数据... \n")
        except Exception as err:
            print(f"更新[{db_name}]配置出错:{err}... \n")
    input("全部结束,按回车关闭...")
