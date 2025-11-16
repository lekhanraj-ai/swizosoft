# Rejection Workflow - Quick Reference

## What Changed

The rejection process now **permanently deletes** all candidate data and documents instead of just updating a status.

---

## For Admins

### How to Reject an Application

1. **Go to** Admin Dashboard → Free/Paid Internship section
2. **Click** the [Reject] button next to a candidate
3. **Review** the modal that appears:
   - Candidate information (name, USN, email)
   - Warning about what will be deleted
   - List of rejection reasons
4. **Select** a rejection reason (e.g., "Does not meet minimum qualifications")
5. **Confirm** the rejection

### What Happens After Rejection

✅ All documents deleted (resume, project, ID proof)
✅ Candidate record removed from database  
✅ Candidate receives rejection email
✅ Dashboard refreshes automatically
✅ Candidate no longer appears in the list

---

## For Developers

### Backend Changes (admin_app.py)

**Endpoint**: `POST /reject/<user_id>?type=free|paid`

**Old Behavior**: Updated status to REJECTED
**New Behavior**: Deletes all records and documents

```python
# Step 1: Delete documents
DELETE FROM free_document_store 
WHERE free_internship_application_id = user_id

# Step 2: Delete application record
DELETE FROM free_internship_application 
WHERE id = user_id

# Step 3: Send rejection email
```

### Frontend Changes (admin_dashboard.js)

**New Function**: `showRejectionModal(internshipId, internshipType)`

```javascript
// Fetches candidate profile
// Fetches rejection reasons
// Shows enhanced modal with:
// - Candidate info
// - Deletion warnings
// - Reason selection
```

### UI Changes (admin_dashboard.html)

Enhanced rejection modal with:
- Candidate Information section
- Red/Orange warning box with details
- Scrollable reasons list
- Cancel button

### Styling Changes (dashboard.css)

New CSS classes:
- `.rejection-candidate-info` - Candidate details display
- `.rejection-warning` - Warning section styling
- `.candidate-details` - Grid layout for info

---

## Database Schema

### Foreign Keys Used

```
free_document_store.free_internship_application_id 
  ↓ (Foreign Key)
free_internship_application.id

paid_document_store.paid_internship_application_id 
  ↓ (Foreign Key)
paid_internship_application.id
```

### Deletion Strategy

1. Delete documents first (BLOBs in document_store)
2. Then delete application record
3. No orphaned records remain

---

## Testing

### Manual Testing Steps

1. **Create a test applicant** in free_internship_application
2. **Go to Admin Dashboard** → Free Internship
3. **Click Reject** button
4. **Verify modal shows**:
   - ✓ Candidate name, USN, email
   - ✓ Warning with deletion details
   - ✓ List of reasons
5. **Select a reason**
6. **Verify in database**:
   ```sql
   SELECT * FROM free_internship_application WHERE usn = 'TEST001';
   -- Should return 0 rows (deleted)
   
   SELECT * FROM free_document_store 
   WHERE free_internship_application_id = 1;
   -- Should return 0 rows (deleted)
   ```
7. **Verify rejection email** was sent

### Automated Test (Example)

```python
# Test that rejection deletes data
response = requests.post(
    'http://localhost:5000/reject/123?type=free',
    data={'reason': 'Does not meet minimum qualifications'}
)
assert response.status_code == 200
assert response.json()['success'] == True

# Verify data is deleted
cursor.execute("SELECT * FROM free_internship_application WHERE id = 123")
assert cursor.fetchone() is None
```

---

## Files Modified

| File | Changes |
|------|---------|
| `admin_app.py` | Updated `/reject` endpoint with DELETE queries |
| `admin_dashboard.html` | Enhanced rejection modal with warning section |
| `admin_dashboard.js` | Updated `showRejectionModal()` to fetch candidate info |
| `dashboard.css` | Added styles for new modal sections |

---

## Error Handling

| Error | Response | Handling |
|-------|----------|----------|
| Email not found | 404 | Return error, don't delete |
| Delete fails | 500 | Log error, return message |
| Email send fails | 500 | Log error but data was deleted |

---

## Important Notes

⚠️ **This is a PERMANENT deletion** - cannot be undone
⚠️ **Regular backups recommended** for data recovery
⚠️ **Works for both** Free and Paid internships
✅ **Email always sent** before deletion

---

## Troubleshooting

### Issue: Rejection button doesn't work

**Solution**: 
- Check browser console for JavaScript errors
- Verify admin is logged in
- Ensure `/admin/api/get-profile` endpoint works

### Issue: Modal shows no candidate info

**Solution**:
- Check `/admin/api/get-profile/<id>` returns data
- Verify applicant exists in database
- Check browser network tab for errors

### Issue: Data not deleted

**Solution**:
- Verify foreign key relationship exists
- Check DELETE permissions in database
- Check database logs for errors

---

## Future Improvements

- [ ] Add soft delete (archive instead of delete)
- [ ] Add audit logging (who rejected, when)
- [ ] Add custom rejection reason option
- [ ] Add batch rejection
- [ ] Add rejection history/analytics

---

## Support

For issues or questions:
1. Check the `REJECTION_WORKFLOW_GUIDE.md` for detailed documentation
2. Review the `REJECTION_WORKFLOW_DIAGRAM.md` for visual flow
3. Check database logs for SQL errors
4. Contact development team
