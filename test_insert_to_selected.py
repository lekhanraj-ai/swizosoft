import pymysql
from config import Config

conn = pymysql.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD, database=Config.MYSQL_DB)
cur = conn.cursor(pymysql.cursors.DictCursor)

try:
    # Fetch up to 5 paid applicants (use SELECT * to adapt to current schema)
    cur.execute("SELECT * FROM paid_internship_application LIMIT 5")
    applicants = cur.fetchall()
    print(f"Found {len(applicants)} paid applicants (sample):")
    for a in applicants:
        print(' ', a)

    for a in applicants:
        user_id = a['id']
        # adaptively read fields from application row
        usn = a.get('usn') or a.get('roll') or a.get('usn_number')
        name = a.get('name') or a.get('full_name') or ''
        application_id = a.get('application_id') or str(user_id)
        print(f"\nProcessing applicant id={user_id}, usn={usn}, name={name}")
        if not usn:
            print('  Skipping: missing USN')
            continue
        # check existing
        cur.execute("SELECT usn FROM Selected WHERE usn = %s LIMIT 1", (usn,))
        if cur.fetchone():
            print(f"  Skipping: USN {usn} already exists in Selected")
            continue
        # Insert
        insert_sql = """INSERT INTO Selected (application_id, name, email, phone, usn, year, qualification, branch, college, domain, project_description, internship_project_name, internship_project_content, project_title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (
            application_id,
            name,
            a.get('email') or '',
            a.get('phone') or '',
            usn,
            a.get('year') or '',
            a.get('qualification') or '',
            a.get('branch') or '',
            a.get('college') or '',
            a.get('domain') or '',
            a.get('project_description') or a.get('project') or '',
            None,
            None,
            None
        )
        try:
            cur.execute(insert_sql, params)
            conn.commit()
            print(f"  Inserted applicant id={user_id} into Selected (usn={usn})")
        except Exception as e:
            print(f"  Error inserting: {e}")

    # Show Selected rows
    cur.execute("SELECT * FROM Selected LIMIT 20")
    rows = cur.fetchall()
    print('\nSelected table now has rows:')
    for r in rows:
        print(' ', r)

finally:
    cur.close()
    conn.close()
