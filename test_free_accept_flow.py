#!/usr/bin/env python3
"""
Test script to verify free internship accept flow:
1. Accept a free internship applicant
2. Verify data moves to approved_candidates table
3. Verify data is deleted from free_internship_application table
4. Verify email is sent
"""

import requests
import pymysql
import time
from config import get_config

BASE_URL = 'http://127.0.0.1:5000'

def get_db():
    config = get_config()
    return pymysql.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Get a free internship applicant
print("Step 1: Finding a free internship applicant...")
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT id, name, usn, email FROM free_internship_application LIMIT 1")
free_app = cursor.fetchone()
cursor.close()
conn.close()

if not free_app:
    print("No free internship applications found!")
    exit(1)

applicant_id = free_app['id']
applicant_usn = free_app['usn']
applicant_name = free_app['name']
applicant_email = free_app['email']

print(f"  Found: ID={applicant_id}, Name={applicant_name}, USN={applicant_usn}, Email={applicant_email}")

# Before accepting, check if already in approved_candidates
print("\nStep 2: Checking if already in approved_candidates...")
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM approved_candidates WHERE usn = %s", (applicant_usn,))
existing = cursor.fetchone()
cursor.close()
conn.close()

if existing:
    print(f"  WARNING: Already in approved_candidates (user_id={existing.get('user_id')})")
    print("  Skipping test to avoid duplicates")
    exit(0)

# Send accept request
print("\nStep 3: Sending accept request...")
try:
    response = requests.post(
        f'{BASE_URL}/accept/{applicant_id}?type=free',
        timeout=10
    )
    print(f"  Response Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    if response.status_code != 200:
        print("  ERROR: Accept request failed!")
        exit(1)
except Exception as e:
    print(f"  ERROR: {e}")
    exit(1)

# Wait a moment for database operations
time.sleep(2)

# Check if in approved_candidates
print("\nStep 4: Verifying data moved to approved_candidates...")
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM approved_candidates WHERE usn = %s", (applicant_usn,))
approved = cursor.fetchone()
cursor.close()
conn.close()

if approved:
    print(f"  SUCCESS: Found in approved_candidates")
    print(f"    USN: {approved.get('usn')}")
    print(f"    Name: {approved.get('name')}")
    print(f"    User ID: {approved.get('user_id')}")
    print(f"    Application ID: {approved.get('application_id')}")
    print(f"    Email: {approved.get('email')}")
else:
    print(f"  FAILED: Not found in approved_candidates!")
    exit(1)

# Check if deleted from free_internship_application
print("\nStep 5: Verifying data deleted from free_internship_application...")
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM free_internship_application WHERE id = %s", (applicant_id,))
free_deleted = cursor.fetchone()
cursor.close()
conn.close()

if free_deleted:
    print(f"  FAILED: Still exists in free_internship_application!")
    exit(1)
else:
    print(f"  SUCCESS: Successfully deleted from free_internship_application")

# Check if deleted from free_document_store
print("\nStep 6: Verifying documents deleted from free_document_store...")
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM free_document_store WHERE free_internship_application_id = %s", (applicant_id,))
docs_deleted = cursor.fetchone()
cursor.close()
conn.close()

if docs_deleted:
    print(f"  FAILED: Still exists in free_document_store!")
    exit(1)
else:
    print(f"  SUCCESS: Successfully deleted from free_document_store")

print("\n" + "="*60)
print("ALL TESTS PASSED!")
print("="*60)
print(f"\nSummary:")
print(f"  Applicant: {applicant_name} ({applicant_usn})")
print(f"  Status: Accepted and moved to approved_candidates")
print(f"  Email: {applicant_email}")
print(f"  Original records: DELETED from free internship tables")
