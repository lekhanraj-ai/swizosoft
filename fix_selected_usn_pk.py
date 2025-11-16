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

    print("Creating backup of current Selected table as Selected_backup2...")
    cursor.execute("CREATE TABLE IF NOT EXISTS Selected_backup2 AS SELECT * FROM Selected")
    conn.commit()
    print("  ✓ Backup created (Selected_backup2)")

    print("Dropping current Selected table...")
    cursor.execute("DROP TABLE IF EXISTS Selected")
    conn.commit()
    print("  ✓ Dropped")

    print("Creating new Selected table with usn as PRIMARY KEY...")
    create_sql = '''
    CREATE TABLE Selected (
        id INT UNIQUE AUTO_INCREMENT,
        application_id VARCHAR(20) UNIQUE,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        usn VARCHAR(20) NOT NULL,
        year VARCHAR(50) NOT NULL,
        qualification VARCHAR(50) NOT NULL,
        branch VARCHAR(100) NOT NULL,
        college VARCHAR(200) NOT NULL,
        domain VARCHAR(100) NOT NULL,
        project_description VARCHAR(255),
        internship_project_name VARCHAR(255),
        internship_project_content MEDIUMBLOB,
        project_title VARCHAR(50),
        approved_date DATE NOT NULL DEFAULT CURDATE(),
        status ENUM('ongoing','completed') NOT NULL DEFAULT 'ongoing',
        completion_date DATE NOT NULL DEFAULT CURDATE(),
        resend_count INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (usn)
    ) ENGINE=InnoDB
    '''
    cursor.execute(create_sql)
    conn.commit()
    print("  ✓ New table created (usn is PRIMARY KEY)")

    print("Restoring data from Selected_backup2 into new Selected (skipping rows with NULL usn)...")
    restore_sql = '''
    INSERT INTO Selected
    (application_id, name, email, phone, usn, year, qualification, branch, college, domain,
     project_description, internship_project_name, internship_project_content, project_title,
     approved_date, status, completion_date, resend_count, created_at)
    SELECT application_id, name, email, phone, usn, year, qualification, branch, college, domain,
     project_description, internship_project_name, project_document_content, project_title,
     approved_date, status, completion_date, resend_count, created_at
    FROM Selected_backup2
    WHERE usn IS NOT NULL AND usn <> ''
    '''
    cursor.execute(restore_sql)
    conn.commit()
    print(f"  ✓ Restored {cursor.rowcount} rows")

    cursor.execute("SELECT COUNT(*) as cnt FROM Selected")
    cnt = cursor.fetchone()['cnt']
    print(f"Total rows in new Selected: {cnt}")

    cursor.close()
    conn.close()
    print('Migration to usn PK completed successfully.')
except Exception as e:
    print('Error during migration:', e)
    import traceback
    traceback.print_exc()
