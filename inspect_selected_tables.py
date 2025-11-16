import pymysql
from config import Config

conn = pymysql.connect(host=Config.MYSQL_HOST,user=Config.MYSQL_USER,password=Config.MYSQL_PASSWORD,database=Config.MYSQL_DB)
cur=conn.cursor(pymysql.cursors.DictCursor)
print('Tables:')
cur.execute("SHOW TABLES")
for r in cur.fetchall(): print(' ', list(r.values())[0])

for t in ['Selected','Selected_backup','Selected_backup2']:
    try:
        print('\nDESC', t)
        cur.execute(f"DESC {t}")
        for row in cur.fetchall(): print(' ', row)
        cur.execute(f"SELECT COUNT(*) as cnt FROM {t}")
        print(' Count:', cur.fetchone()['cnt'])
        print(' Sample rows:')
        cur.execute(f"SELECT * FROM {t} LIMIT 5")
        for row in cur.fetchall(): print(' ', row)
    except Exception as e:
        print(f'  (not found or error) {e}')

cur.close(); conn.close()
