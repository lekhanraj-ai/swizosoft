# Rejection Workflow Implementation Guide

## Overview
This document describes the complete rejection workflow for internship applications in Swizosoft. When an admin rejects an application, all candidate data and documents are **permanently deleted** from the database.

---

## Database Structure

### Free Internship Tables
- **free_internship_application**: Contains candidate information
  - Columns: `id`, `name`, `usn`, `email`, `phone`, `year`, `branch`, `college`, etc.
  - `id` is the primary key (auto-increment)

- **free_document_store**: Contains file BLOBs (documents)
  - Foreign Key: `free_internship_application_id` → `free_internship_application.id`
  - Columns: `resume_content`, `project_document_content`, `id_proof_content` (all LONGBLOB)

### Paid Internship Tables
- **paid_internship_application**: Same structure as free
- **paid_document_store**: Same structure as free (uses `paid_internship_application_id` FK)

---

## Rejection Workflow Steps

### Step 1: Admin Clicks Reject Button
- Location: Admin Dashboard (`/admin/dashboard`)
- The admin views a list of applicants and clicks the **"Reject"** button for a candidate

### Step 2: Rejection Modal Opens
The modal displays:
1. **Candidate Information**
   - Name
   - USN (Student ID)
   - Email
   
2. **Warning Section** (Red/Orange alert box)
   - ⚠️ Warning that rejection will:
     - Permanently delete the resume
     - Permanently delete the project document
     - Permanently delete the ID proof
     - Completely remove all records from the database
     - Send a rejection email to the candidate
   - Emphasizes: **"This action cannot be undone!"**

3. **Rejection Reasons List**
   - Pre-defined reasons to choose from:
     - Does not meet minimum qualifications
     - Lack of relevant experience
     - Poor communication skills
     - Scheduling conflict
     - Position filled
     - And 10 more...

### Step 3: Admin Selects Rejection Reason
- Admin clicks on one of the rejection reasons
- Modal closes and rejection is processed

### Step 4: Backend Processing
The `/reject/<user_id>` endpoint:

1. **Fetches** applicant contact info (email, name)
2. **Deletes** from document store (all BLOBs)
   ```sql
   DELETE FROM free_document_store 
   WHERE free_internship_application_id = <user_id>
   ```

3. **Deletes** from application table (all candidate records)
   ```sql
   DELETE FROM free_internship_application 
   WHERE id = <user_id>
   ```

4. **Sends** rejection email with the selected reason
5. **Returns** success message

### Step 5: Dashboard Refreshes
- The table automatically reloads
- Rejected candidate no longer appears in the list

---

## API Endpoints

### Get Rejection Reasons
```
GET /admin/api/get-rejection-reasons
Response:
{
    "success": true,
    "reasons": [
        "Does not meet minimum qualifications",
        "Lack of relevant experience",
        ...
    ]
}
```

### Get Candidate Profile
```
GET /admin/api/get-profile/<id>?type=free|paid
Response:
{
    "success": true,
    "data": {
        "id": 1,
        "name": "John Doe",
        "usn": "USN001",
        "email": "john@example.com",
        ...
    }
}
```

### Reject Application
```
POST /reject/<id>?type=free|paid
Body: FormData with "reason" field
Response:
{
    "success": true,
    "message": "Application rejected and all data deleted. Rejection email sent"
}
```

---

## File Changes

### 1. `admin_app.py` - Backend Logic
**Function**: `admin_reject(user_id)`
**Changes**:
- Replaced status UPDATE with DELETE queries
- Deletes from both `document_store` and `application` tables
- Uses proper foreign key relationships for cascading deletes
- Improved error handling and logging

```python
# Deletes all documents first
DELETE FROM {doc_store_table} 
WHERE free_internship_application_id = %s

# Then deletes the application record
DELETE FROM {app_table} 
WHERE id = %s
```

### 2. `templates/admin_dashboard.html` - UI
**Changes**:
- Enhanced rejection modal with new sections:
  - Candidate information display
  - Warning section with checklist
  - Rejection reasons list
- Added proper structure and styling

### 3. `static/js/admin_dashboard.js` - Frontend Logic
**Function**: `showRejectionModal(internshipId, internshipType)`
**Changes**:
- Fetches candidate profile data before showing modal
- Populates candidate name, USN, and email in the modal
- Fetches and displays rejection reasons
- Improved user experience with pre-filled information

### 4. `static/css/dashboard.css` - Styling
**Changes**:
- Added styles for candidate information section
- Enhanced warning section styling (red/orange theme)
- Improved modal layout and scrolling for longer content
- Better visual hierarchy for warnings and reasons

---

## Data Deletion Safety

### Cascade Delete Strategy
1. **Document Store First**: Deletes all BLOB data (resume, project, ID proof)
2. **Application Table Second**: Deletes candidate record

### Foreign Key Relationships
- `document_store` table uses `free_internship_application_id` as FK
- When candidate is deleted, all associated documents are deleted

### Database Integrity
- No orphaned records left behind
- Complete cleanup of all related data
- Transactional delete operations with proper error handling

---

## Email Notification

When a candidate is rejected:
1. Rejection email is sent to candidate's email address
2. Email includes the selected rejection reason
3. Email is sent from: `no-reply2@swizosoft.in`

### Email Template
The email informs the candidate:
- Their application has been rejected
- Reason for rejection
- Encouragement to apply again in future

---

## User Journey Example

### Scenario: Rejecting "Rahul Kumar"
1. Admin views Free Internship dashboard
2. Finds row: `Rahul Kumar | USN123 | [View Docs] [Actions]`
3. Clicks **Reject** button
4. Modal appears showing:
   - Name: Rahul Kumar
   - USN: USN123
   - Email: rahul@example.com
   - Warning: "Rejecting will permanently delete all data!"
   - Reasons list to choose from
5. Admin selects reason: "Does not meet minimum qualifications"
6. Popup closes
7. Success message: "Application rejected and all data deleted. Rejection email sent"
8. Dashboard refreshes
9. Rahul Kumar no longer appears in the table
10. All his documents (resume, project, ID) are permanently deleted from database
11. Rahul receives rejection email with the reason

---

## Error Handling

The rejection endpoint handles:
- Missing applicant email → 404 error
- Database deletion failures → 500 error with description
- Email sending failures → 500 error with message
- Invalid application type (free/paid) → proper table resolution

---

## Testing Checklist

- [x] Rejection modal displays candidate information correctly
- [x] Warning section clearly shows what will be deleted
- [x] Rejection reasons load and display properly
- [x] Clicking a reason triggers deletion
- [x] All records deleted from database
- [x] Documents deleted from document_store table
- [x] Application record deleted from application table
- [x] Rejection email sent successfully
- [x] Dashboard refreshes after rejection
- [x] Rejected candidate no longer in list
- [x] Works for both free and paid internships

---

## Rollback/Recovery

**Important**: Since this is a permanent deletion:
- No automatic rollback mechanism
- Database backups are critical
- Consider implementing:
  - Regular automated backups
  - Soft delete option (archive instead of delete)
  - Admin audit logs

---

## Future Enhancements

1. **Soft Delete**: Archive rejected applications instead of deleting
2. **Audit Logging**: Track who rejected and when
3. **Batch Rejection**: Reject multiple candidates at once
4. **Custom Reason**: Allow admin to enter custom rejection reason
5. **Rejection History**: Maintain history of rejections for analytics

---

## Support

For issues or questions about the rejection workflow, contact the development team.
