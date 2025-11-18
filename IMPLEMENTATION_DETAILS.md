# Implementation Details - Offer Letter Automation

## Summary of Changes

### Issue 1: Role Storage ✅ FIXED

**Problem**: Roles might store as "int" instead of "intern"
**Solution**: Code already uses `f"{domain_val} Intern"` which correctly stores the full word "Intern"
**Locations**:

- Line 1286 in admin_app.py (free internships)
- Line 1680 in admin_app.py (paid internships)
  **Status**: Already correct, no changes needed

### Issue 2: Domain Change Modal ✅ ENHANCED

**Problem**: Domain change needed to be part of the acceptance flow
**Solution**: Already exists - enhanced by adding internship type modal as next step
**Change**: Modified `adminAccept()` to show internship type modal instead of directly accepting
**File**: templates/admin_approved_candidates.html

### Issue 3: Internship Type Selection ✅ NEW

**Problem**: Needed to select between remote, hybrid, and on-site internships
**Solution**: Created new modal with three options
**Implementation**:

1. Added `internshipTypeModal` div (lines 484-565)
2. Added `closeInternshipTypeModal()` function
3. Added `confirmInternshipType()` function
4. Modified `adminAccept()` to show modal instead of direct accept

**File**: templates/admin_approved_candidates.html
**Lines**:

- Modal HTML: 484-565
- JavaScript: 1002-1050

### Issue 4: Backend Handler Update ✅ UPDATED

**Problem**: Need to accept internship_type parameter and store it
**Solution**: Modified `handle_approved_candidate_accept()` function
**Changes**:

```python
# Before
def handle_approved_candidate_accept(approved_candidate):

# After
def handle_approved_candidate_accept(approved_candidate, internship_type='free'):
    # Now accepts and stores internship_type
    # Generates offer letter automatically
```

**Implementation Details**:

1. Added `internship_type` parameter (default='free')
2. Updated INSERT/UPDATE queries to include `mode_of_internship`
3. Set correct `completion_date` based on type (1 month for free, 3 for others)
4. Added automatic offer letter generation via API call
5. Added error handling for failed generation (doesn't block candidate acceptance)

**File**: admin_app.py
**Lines**:

- Function signature: 1267
- Parameter handling: 1277-1283
- INSERT query: 1334-1337
- API call: 1380-1410

### Issue 5: Accept Route Enhancement ✅ UPDATED

**Problem**: /accept route needed to extract and pass internship_type
**Solution**: Parse internship_type from request and pass to handler
**Changes**:

```python
@app.route('/accept/<int:user_id>', methods=['POST'])
def admin_accept(user_id):
    # Extract internship type from request
    internship_type = 'free'
    if request.is_json:
        internship_type = request.get_json().get('internship_type', 'free')
    elif request.form:
        internship_type = request.form.get('internship_type', 'free')

    # Pass to handler
    return handle_approved_candidate_accept(approved_candidate, internship_type)
```

**File**: admin_app.py
**Lines**: 1415-1440

### Issue 6: Offer Letter Generation ✅ NEW

**Problem**: Manual data entry in HTML form for each offer letter
**Solution**: Automatic generation via API when candidate accepted
**Implementation**:

1. Extract candidate data from Selected table after insert
2. Call `/api/generate-offer` endpoint on offer-letter-generator service
3. Handle success/failure (doesn't block acceptance)

**Code** (admin_app.py, lines 1380-1410):

```python
try:
    import requests
    offer_letter_data = {
        'name': name_val,
        'usn': usn_val,
        'email': email_val,
        'college': college_val,
        'role': role_val,
        'duration': '3 months',
        'internship_type': internship_type
    }

    response = requests.post(
        'http://localhost:5001/api/generate-offer',
        json=offer_letter_data,
        timeout=30
    )
except Exception as e:
    app.logger.warning(f"Offer letter generation error: {e}")
```

### Issue 7: Offer Generator Refactoring ✅ NEW

**Problem**: PDF generation logic tightly coupled to form submission
**Solution**: Extract into reusable function and add API endpoint
**Changes**:

1. **New Function**: `generate_offer_pdf()`

   - Parameters: name, usn, college, email, role, duration, intern_type
   - Returns: (pdf_file_path, reference_number)
   - Contains all PDF generation logic

2. **Original Endpoint**: `/generate-offer` (unchanged)

   - Calls `generate_offer_pdf()` internally
   - Returns PDF as file download
   - Used by HTML form

3. **New API Endpoint**: `/api/generate-offer`
   - Accepts JSON data
   - Calls `generate_offer_pdf()`
   - Returns JSON with base64 PDF
   - Used by admin_app for automation

**File**: offer-letter-generator/app.py
**Lines**:

- Function: 68-353
- Old endpoint: 355-361
- New endpoint: 362-415

## Data Flow Diagram

```
┌─────────────────────────────────────────────────┐
│     Admin Dashboard - Approved Candidates       │
└─────────────────────────────────────────────────┘
            │
            │ Click "Accept"
            ↓
┌─────────────────────────────────────────────────┐
│   Modal 1: Domain Change (existing)             │
│   - Shows current domain                        │
│   - Dropdown to select new domain              │
│   - Cancel / Accept buttons                    │
└─────────────────────────────────────────────────┘
            │
            │ adminAccept(id, newDomain)
            │ (from confirmAcceptWithDomain)
            ↓
┌─────────────────────────────────────────────────┐
│   Modal 2: Internship Type Selection (NEW)      │
│   - Remote-based opportunity                   │
│   - Hybrid-based opportunity                   │
│   - On-site based opportunity                  │
│   - Cancel / Proceed buttons                   │
└─────────────────────────────────────────────────┘
            │
            │ confirmInternshipType()
            │ POST /accept/{user_id}
            │ {internship_type: selected_type}
            ↓
┌─────────────────────────────────────────────────┐
│         admin_app.py - admin_accept()           │
│ 1. Extract internship_type from request        │
│ 2. Check if approved candidate                 │
│ 3. Call handle_approved_candidate_accept()    │
└─────────────────────────────────────────────────┘
            │
            ↓
┌─────────────────────────────────────────────────┐
│  handle_approved_candidate_accept()             │
│ 1. Generate candidate_id (SIN25FD001)          │
│ 2. INSERT/UPDATE Selected table                │
│ 3. Store mode_of_internship = selected_type    │
│ 4. DELETE from approved_candidates             │
│ 5. Call offer letter API                       │
└─────────────────────────────────────────────────┘
            │
            │ POST to localhost:5001
            │ /api/generate-offer
            ↓
┌─────────────────────────────────────────────────┐
│   offer-generator - api_generate_offer()       │
│ 1. Validate all required fields                │
│ 2. Call generate_offer_pdf()                   │
│ 3. Generate unique reference number            │
│ 4. Create PDF file                             │
│ 5. Return JSON with base64 PDF                 │
└─────────────────────────────────────────────────┘
            │
            ↓
   ┌────────────────────────┐
   │ Success Response:      │
   │ {                      │
   │   success: true,       │
   │   reference_number:... │
   │   pdf_data: base64...  │
   │ }                      │
   └────────────────────────┘
```

## Database Changes

### Selected Table - mode_of_internship Field

Before: `'free'` or `'paid'` (limited options)

After: Can be any of:

- `'free'` (backward compatible)
- `'paid'` (backward compatible)
- `'remote-based opportunity'` (NEW)
- `'hybrid-based opportunity'` (NEW)
- `'on-site based opportunity'` (NEW)

### SQL Query Example

```sql
-- Insert new accepted candidate
INSERT INTO Selected (
    candidate_id, name, email, phone, usn, year,
    qualification, branch, college, domain, roles,
    approved_date, status, completion_date, mode_of_internship
) VALUES (
    'SIN25FD001',          -- Generated ID
    'John Doe',            -- Name
    'john@email.com',      -- Email
    '+91-9876543210',      -- Phone
    'CS12345',             -- USN
    '3',                   -- Year
    'B.Tech',              -- Qualification
    'Computer Science',    -- Branch
    'IIIT Bangalore',      -- College
    'FULL STACK DEVELOPER',-- Domain
    'FULL STACK DEVELOPER Intern', -- Role (with full "Intern")
    CURDATE(),             -- Approved date
    'ongoing',             -- Status
    DATE_ADD(CURDATE(), INTERVAL 3 MONTH), -- Completion date
    'remote-based opportunity'  -- NEW: Selected internship type
);
```

## Error Handling

### If Offer Letter Generation Fails

- Error logged in admin_app
- Candidate STILL accepted (no rollback)
- Selected table updated successfully
- Offer letter can be generated later manually
- User sees success message anyway

### If Offer Generator Service Not Running

- Connection error logged
- Candidate accepted normally
- Message: "Could not connect to offer-letter-generator service on localhost:5001"
- Offer letter generation skipped (non-blocking error)

### If Required Fields Missing

- API returns 400 error
- Request logged with missing fields
- Candidate acceptance still completes
- Offer letter generation fails gracefully

## Testing Instructions

### Setup

```bash
# Terminal 1
cd ~/swizosoft
python admin_app.py

# Terminal 2
cd ~/swizosoft/offer-letter-generator
python app.py
```

### Test Flow

1. Open http://localhost:5000/admin/dashboard
2. Go to "Approved Candidates"
3. Click "Accept" on any candidate
4. Select new domain (or keep current)
5. Select internship type
6. Watch console for success message
7. Check offer-letter-generator/generated/ for PDF

### Verification Queries

```sql
-- Check Selected table
SELECT candidate_id, name, usn, role, mode_of_internship,
       approved_date, status
FROM Selected
WHERE usn = 'TESTUSN'
ORDER BY approved_date DESC LIMIT 1;

-- Check internship type was stored
SELECT mode_of_internship FROM Selected
WHERE candidate_id = 'SIN25FD001';
```

## Files Modified

### 1. templates/admin_approved_candidates.html

**Lines Changed**: ~200 lines
**Changes**:

- Added internship type modal (lines 484-565)
- Updated JavaScript functions (lines 984-1050)
- New modal handlers and flow

**Key Functions**:

- `closeInternshipTypeModal()` - closes modal
- `confirmInternshipType()` - handles selection
- `adminAccept()` - modified to show modal

### 2. admin_app.py

**Lines Changed**: ~150 lines
**Changes**:

- Modified `handle_approved_candidate_accept()` (lines 1267-1410)
- Updated `/accept/<user_id>` route (lines 1415-1450)
- Added offer letter API call (lines 1380-1410)

**Key Updates**:

- Added `internship_type` parameter
- Added mode_of_internship to INSERT/UPDATE
- Added offer letter generation call
- Added error handling for API

### 3. offer-letter-generator/app.py

**Lines Changed**: ~300 lines
**Changes**:

- Refactored to `generate_offer_pdf()` (lines 68-353)
- Updated original `/generate-offer` (lines 355-361)
- Added new `/api/generate-offer` (lines 362-415)

**Key Functions**:

- `generate_offer_pdf()` - reusable PDF generation
- `/api/generate-offer` - JSON API endpoint

## Backward Compatibility

✅ All changes are backward compatible:

- Old `/generate-offer` form endpoint still works
- `mode_of_internship` field handles old values ('free', 'paid')
- Database migrations not required
- No breaking changes to existing APIs

## Next Steps (Optional)

1. **Store PDF reference**: Add offer_letter_path to Selected table
2. **Email integration**: Send PDF to candidate via email
3. **Batch generation**: Generate for multiple candidates
4. **Digital signature**: Add to PDF
5. **Template variants**: Different templates per domain
6. **Download from dashboard**: Allow re-download of generated PDFs

---

**Status**: ✅ IMPLEMENTATION COMPLETE
**Test Status**: Ready for QA
**Date**: November 18, 2025
