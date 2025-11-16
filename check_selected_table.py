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
    
    # Check table structure
    cursor.execute('DESC Selected')
    rows = cursor.fetchall()
    print('Selected Table Structure:')
    for row in rows:
        print(f'  {row}')
    
    # Check constraints
    cursor.execute("SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME='Selected'")
    constraints = cursor.fetchall()
    print('\nConstraints:')
    for c in constraints:
        print(f'  {c}')
    
    # Check unique keys
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME='Selected'")
    keys = cursor.fetchall()
    print('\nKey Column Usage:')
    for k in keys:
        print(f'  {k}')
    
    # Count current rows
    cursor.execute('SELECT COUNT(*) as count FROM Selected')
    count_result = cursor.fetchone()
    print(f'\nCurrent rows in Selected: {count_result["count"]}')
    
    # Show current data - without id field
    cursor.execute('SELECT application_id, name, email, usn FROM Selected LIMIT 10')
    data = cursor.fetchall()
    print('\nCurrent data in Selected:')
    for row in data:
        print(f'  {row}')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
