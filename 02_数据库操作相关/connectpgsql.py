import psycopg2

# psycopg2 postgreSQL包
conn = psycopg2.connect(database="n2db",user="n2admin",password="fefdee",
                        host="ip",port="5432")
cur = conn.cursor()
sql = "select * from t_cth_test"
cur.execute(sql)
results = cur.fetchall()
print(results)
conn.close()