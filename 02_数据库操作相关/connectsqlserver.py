import pymssql


conn = pymssql.connect(host='', user='sa', password='', database='demo', charset='utf8')
cursor = conn.cursor()
print(111)
cursor.execute("select * from userInfo")
print (cursor.fetchall())
cursor.close()
conn.close()

