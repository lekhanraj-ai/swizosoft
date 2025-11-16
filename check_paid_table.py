import pymysql
from config import Config

try:
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # Check what tables exist
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Available tables:")
    for t in tables:
        print(f"  {list(t.values())[0]}")
    
    # Check paid_internship_application structure
    cursor.execute("DESC paid_internship_application")
    rows = cursor.fetchall()
    print("\npaid_internship_application structure:")
    for row in rows:
        print(f"  {row}")
    
    # Check data
    cursor.execute("SELECT id, name, usn, email FROM paid_internship_application LIMIT 5")
    data = cursor.fetchall()
    print("\nSample data from paid_internship_application:")
    for row in data:
        print(f"  {row}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
