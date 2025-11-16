import pymysql, requests, json
from config import Config

conn = pymysql.connect(host=Config.MYSQL_HOST,user=Config.MYSQL_USER,password=Config.MYSQL_PASSWORD,database=Config.MYSQL_DB)
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute("SELECT id, name, usn FROM paid_internship_application")
apps = cur.fetchall()
cur.execute("SELECT usn FROM Selected")
sel = {r['usn'] for r in cur.fetchall()}
print('Selected USNs count:', len(sel))
candidate = None
for a in apps:
    u = a.get('usn')
    if u and u not in sel:
        candidate = a
        break
if not candidate:
    print('No paid applicant with USN not in Selected found. Listing paid apps:')
    print(json.dumps(apps, default=str, indent=2))
    cur.close(); conn.close(); raise SystemExit
print('Found candidate to test:', candidate)
user_id = candidate['id']
url = f'http://127.0.0.1:5000/accept/{user_id}?type=paid'
print('POST', url)
try:
    r = requests.post(url, timeout=10)
    try:
        print('Status:', r.status_code)
        print('JSON:', r.json())
    except Exception:
        print('Response text:', r.text)
except Exception as e:
    print('HTTP error:', e)

cur.close(); conn.close()
