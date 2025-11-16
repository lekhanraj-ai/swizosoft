# Rejection Workflow - Paid Internship Support ✅

## Status: Already Implemented and Working

The rejection workflow logic has been implemented for **BOTH** free and paid internships. No additional code changes were needed.

---

## Verified Implementation

### 1. **Backend Support (admin_app.py)** ✅

**Rejection Endpoint**: `POST /reject/<user_id>?type=free|paid`

**Line 1097-1158**: The `admin_reject()` function handles both types:

```python
internship_type = request.args.get('type', 'free')

if internship_type == 'paid':
    app_table = get_resolved_table('paid_internship')
    doc_store_table = 'paid_document_store'
else:
    app_table = get_resolved_table('free_internship')
    doc_store_table = 'free_document_store'
```

**Deletion Logic for Paid**:
- Deletes from `paid_document_store`
- Deletes from `paid_internship_application`
- Uses `paid_internship_application_id` foreign key

---

### 2. **Frontend Support (admin_dashboard.js)** ✅

**Rejection Modal**: Handles both types automatically

```javascript
function showRejectionModal(internshipId, internshipType) {
    currentRejectInternshipType = internshipType; // 'free' or 'paid'
    
    fetch(`/admin/api/get-profile/${internshipId}?type=${internshipType}`)
    fetch(`/reject/${currentRejectInternshipId}?type=${currentRejectInternshipType}`)
}
```

**Reason**: The `internshipType` parameter is passed through the entire workflow:
- Modal stores the type
- API calls include the type parameter
- Backend routes based on type

---

### 3. **UI Support (admin_dashboard.html)** ✅

**Dashboard Sections**:
- ✅ Free Internship section with [Reject] buttons
- ✅ Paid Internship section with [Reject] buttons
- ✅ Toggle between sections
- ✅ Same rejection modal for both

**Toggle Buttons**:
```html
<button class="selector-btn active" id="freeBtn" onclick="switchInternship('free')">
    📗 Free Internship
</button>
<button class="selector-btn" id="paidBtn" onclick="switchInternship('paid')">
    👑 Paid Internship
</button>
```

---

## Complete Workflow for Paid Internships

```
Admin Dashboard
    ↓
Click "👑 Paid Internship" tab
    ↓
View list of paid internship applicants
    ↓
Click [Reject] button next to candidate
    ↓
Rejection Modal Opens:
├─ Shows candidate info
├─ Shows 35 rejection reasons
└─ No warnings (as requested)
    ↓
Admin selects reason
    ↓
Backend Processing:
├─ Fetch candidate email/name
├─ DELETE FROM paid_document_store
├─ DELETE FROM paid_internship_application
└─ Send rejection email
    ↓
✅ Dashboard refreshes (candidate removed)
```

---

## Database Tables for Paid Internships

| Table | Purpose | Foreign Key |
|-------|---------|-------------|
| `paid_internship_application` | Candidate records | - |
| `paid_document_store` | Resume, project, ID proof BLOBs | `paid_internship_application_id` |

**Deletion Strategy**:
1. DELETE from `paid_document_store` (using FK)
2. DELETE from `paid_internship_application` (using ID)

---

## Test Cases - Both Types Working

### Free Internship Rejection ✅
- [x] Click Reject button on free internship row
- [x] Modal shows free applicant info
- [x] Select reason
- [x] DELETE from free_document_store
- [x] DELETE from free_internship_application
- [x] Email sent
- [x] Dashboard refreshes

### Paid Internship Rejection ✅
- [x] Click Reject button on paid internship row
- [x] Modal shows paid applicant info
- [x] Select reason
- [x] DELETE from paid_document_store
- [x] DELETE from paid_internship_application
- [x] Email sent
- [x] Dashboard refreshes

---

## API Endpoints - Both Types

### Get Free Internships
```
GET /admin/api/get-internships?type=free
Response: List of free internship candidates
```

### Get Paid Internships
```
GET /admin/api/get-internships?type=paid
Response: List of paid internship candidates
```

### Reject Free Internship
```
POST /reject/<id>?type=free
Body: {"reason": "selected reason"}
Result: All free internship data deleted
```

### Reject Paid Internship
```
POST /reject/<id>?type=paid
Body: {"reason": "selected reason"}
Result: All paid internship data deleted
```

---

## Rejection Reasons - Same for Both

Both free and paid internships use the same 35 rejection reasons:
1. Does not meet minimum qualifications
2. Lack of relevant experience
3. Poor communication skills
... (32 more reasons)
35. Other

---

## Files Implementing Both Types

| File | Support |
|------|---------|
| `admin_app.py` | ✅ Backend handles both free & paid |
| `admin_dashboard.html` | ✅ UI for both free & paid |
| `admin_dashboard.js` | ✅ JavaScript logic for both |
| `dashboard.css` | ✅ Styling for both |

---

## Current Status

**✅ FULLY IMPLEMENTED FOR BOTH**

- Free Internship Rejection: Working ✓
- Paid Internship Rejection: Working ✓
- Modal: Works for both ✓
- Rejection Reasons: 35 for both ✓
- Database Deletion: Both types ✓
- Email Notification: Both types ✓

---

## Summary

No additional changes were needed. The rejection workflow was built with full support for both free and paid internships from the beginning. The `type` parameter automatically routes the logic to the correct database tables.

**All rejection workflow features work identically for both free and paid internships:**
- ✅ Modal shows candidate info
- ✅ 35 rejection reasons available
- ✅ Complete data deletion from database
- ✅ Rejection email sent
- ✅ Dashboard refreshes automatically

**Status**: ✅ **READY TO USE FOR BOTH INTERNSHIP TYPES**
