#!/usr/bin/env python3
"""Quick test to check if Selected table exists and has data"""
import pymysql
import pymysql.cursors

# Connect to DB using same credentials as admin_app.py
try:
    conn = pymysql.connect(
        host='srv1128.hstgr.io',
        user='u973091162_swizosoft_int',
        password='Internship@Swizosoft1',
        database='u973091162_internship_swi',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    cursor = conn.cursor()
    
    print("✓ Connected to database")
    
    # Check if Selected table exists
    try:
        cursor.execute("SELECT * FROM Selected LIMIT 10")
        rows = cursor.fetchall()
        print(f"✓ Selected table exists with {len(rows)} rows")
        if rows:
            print(f"  First row keys: {list(rows[0].keys())}")
            print(f"  First row data: {rows[0]}")
        else:
            print("  (No rows in Selected)")
    except Exception as e:
        print(f"✗ Error querying Selected: {e}")
    
    # Check what tables exist
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\nTables in database:")
    for t in tables:
        table_name = list(t.values())[0]
        print(f"  - {table_name}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")
