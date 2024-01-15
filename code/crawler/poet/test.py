import pymysql

conn = pymysql.connect( host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='chinesepoetry',
                        charset="utf8")

cursor = conn.cursor()
cursor.execute(''' select name,poem_sum from poet order by poem_sum desc''')
a = cursor.fetchall()[0:100]
x = []
for i in range(100):
    tmp = list(a[i])
    
    x.append(tmp)
print(x[0:50])
