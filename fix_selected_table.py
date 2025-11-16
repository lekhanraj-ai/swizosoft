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
    
    # Step 1: Create a backup of Selected table
    print("Step 1: Creating backup of Selected table...")
    cursor.execute("CREATE TABLE Selected_backup AS SELECT * FROM Selected")
    conn.commit()
    print("  ✓ Backup created as Selected_backup")
    
    # Step 2: Drop the old Selected table
    print("\nStep 2: Dropping old Selected table...")
    cursor.execute("DROP TABLE Selected")
    conn.commit()
    print("  ✓ Old Selected table dropped")
    
    # Step 3: Create new Selected table with proper schema
    print("\nStep 3: Creating new Selected table with auto-increment id...")
    create_sql = """
    CREATE TABLE Selected (
        id INT PRIMARY KEY AUTO_INCREMENT,
        application_id VARCHAR(20) NOT NULL UNIQUE,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        usn VARCHAR(20),
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_sql)
    conn.commit()
    print("  ✓ New Selected table created with schema:")
    print("    - id: INT AUTO_INCREMENT PRIMARY KEY")
    print("    - application_id: VARCHAR(20) UNIQUE (for preventing duplicates)")
    print("    - All other columns as before")
    
    # Step 4: Restore data from backup
    print("\nStep 4: Restoring data from backup...")
    restore_sql = """
    INSERT INTO Selected 
    (application_id, name, email, phone, usn, year, qualification, branch, college, domain,
     project_description, internship_project_name, internship_project_content, project_title,
     approved_date, status, completion_date, resend_count)
    SELECT 
    application_id, name, email, phone, usn, year, qualification, branch, college, domain,
    project_description, internship_project_name, internship_project_content, project_title,
    approved_date, status, completion_date, resend_count
    FROM Selected_backup
    """
    cursor.execute(restore_sql)
    conn.commit()
    print(f"  ✓ Restored {cursor.rowcount} row(s) from backup")
    
    # Step 5: Verify the new table
    print("\nStep 5: Verifying new Selected table...")
    cursor.execute("SELECT COUNT(*) as count FROM Selected")
    result = cursor.fetchone()
    print(f"  ✓ Total rows in Selected: {result['count']}")
    
    cursor.execute("SELECT id, application_id, name, email FROM Selected")
    rows = cursor.fetchall()
    print("\n  Current data in Selected:")
    for row in rows:
        print(f"    ID: {row['id']}, App ID: {row['application_id']}, Name: {row['name']}, Email: {row['email']}")
    
    cursor.execute("DESC Selected")
    schema = cursor.fetchall()
    print("\n  New table schema:")
    for col in schema:
        key_info = f" [{col['Key']}]" if col['Key'] else ""
        print(f"    - {col['Field']}: {col['Type']}{key_info}")
    
    print("\n✅ Migration completed successfully!")
    print("Now the Selected table can store multiple user records with different USNs")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
