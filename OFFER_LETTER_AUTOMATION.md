# Offer Letter Automation - Implementation Summary

## Overview

Automated the offer letter generation process by integrating the admin application with the offer-letter-generator service. When an admin accepts an approved candidate, the system now:

1. Asks if they want to change the candidate's domain
2. Asks to select the internship type (Remote, Hybrid, or On-site)
3. Stores the data in the Selected table with the correct internship type
4. Automatically generates and stores the offer letter PDF

## Changes Made

### 1. **Admin Dashboard UI (admin_approved_candidates.html)**

#### Added Internship Type Modal

- New modal (`internshipTypeModal`) that appears after domain selection
- Three internship type options:
  - Remote-based opportunity
  - Hybrid-based opportunity
  - On-site based opportunity

#### Updated JavaScript Functions

- **Modified `adminAccept()` function**: Now shows the internship type modal instead of directly accepting
- **Added `closeInternshipTypeModal()` function**: Closes the internship type modal
- **Added `confirmInternshipType()` function**: Handles the flow:
  1. Validates internship type selection
  2. Sends acceptance request with internship type
  3. Shows completion message when offer letter generation starts

#### Flow Sequence

```
User clicks "Accept"
  ↓
Shows Domain Change Modal (existing)
  ↓
User selects domain (or keeps current)
  ↓
Shows Internship Type Modal (NEW)
  ↓
User selects internship type
  ↓
System accepts candidate & generates offer letter
```

### 2. **Admin Backend (admin_app.py)**

#### Updated `handle_approved_candidate_accept()` Function

- **Added `internship_type` parameter**: Accepts the selected internship type
- **Fixed role storage**: Ensures roles are stored as "{domain} Intern" (with full "Intern" word)
- **Added duration handling**: Sets completion_date based on internship type:
  - Free internships: 1 month
  - Paid/specified types: 3 months
- **Added offer letter generation**: Automatically calls offer-letter-generator API
- **Stores mode_of_internship**: Saves the selected internship type in the Selected table

#### Updated `admin_accept()` Route

- **Extract internship_type**: Gets the internship type from the request (JSON or form data)
- **Pass to handler**: Forwards internship_type to `handle_approved_candidate_accept()`

#### Offer Letter Auto-Generation

When a candidate is accepted:

```python
offer_letter_data = {
    'name': name_val,
    'usn': usn_val,
    'email': email_val,
    'college': college_val,
    'role': role_val,
    'duration': '3 months',
    'internship_type': internship_type
}

# Calls: POST http://localhost:5001/api/generate-offer
```

### 3. **Offer Letter Generator (offer-letter-generator/app.py)**

#### Refactored PDF Generation

- **Extracted `generate_offer_pdf()` function**:
  - Contains all PDF generation logic
  - Returns tuple: (pdf_file_path, reference_number)
  - Reusable for both web and API calls

#### New API Endpoint: `/api/generate-offer`

- **Method**: POST
- **Input**: JSON with candidate data

  - `name` or `candidate`: Candidate name
  - `usn`: University Serial Number
  - `college`: College name
  - `email`: Email address
  - `role`: Internship role
  - `duration`: Internship duration (default: "3 months")
  - `internship_type`: Type of internship (remote/hybrid/on-site)

- **Output**: JSON response

  ```json
  {
    "success": true,
    "message": "Offer letter generated successfully",
    "reference_number": "SZS/OFFR/2025/NOV/001",
    "filename": "SZS_OFFR_2025_NOV_001.pdf",
    "pdf_data": "<base64_encoded_pdf>"
  }
  ```

- **Features**:
  - Validates all required fields
  - Generates unique reference number (SZS/OFFR/YEAR/MONTH/SERIAL)
  - Returns PDF as base64 encoded data
  - Stores PDF in generated/ folder

#### Backward Compatibility

- Original `/generate-offer` endpoint still works with form data
- New API endpoint doesn't interfere with existing functionality

## Database Schema Changes

### Selected Table Updates

The `mode_of_internship` field now stores:

- `'remote-based opportunity'` - for remote internships
- `'hybrid-based opportunity'` - for hybrid internships
- `'on-site based opportunity'` - for on-site internships
- `'free'` - for free internships (backward compatible)
- `'paid'` - for paid internships (backward compatible)

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Admin Dashboard - Approved Candidates Page                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
                  User clicks "Accept"
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Modal 1: Domain Selection (existing)                         │
│ - Current Domain: [Domain shown]                            │
│ - New Domain: [Dropdown with options]                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
                 User selects domain or keeps current
                            ↓
                 System updates domain in approved_candidates
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Modal 2: Internship Type Selection (NEW)                    │
│ - Remote-based opportunity                                  │
│ - Hybrid-based opportunity                                  │
│ - On-site based opportunity                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
                  User selects internship type
                            ↓
        POST /accept/{user_id} with internship_type
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ admin_app.py - handle_approved_candidate_accept()          │
│ 1. Generate unique candidate_id (SIN25FD001)               │
│ 2. Insert into Selected table                              │
│ 3. Store mode_of_internship with selected type            │
│ 4. Call offer-letter-generator API                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
        POST http://localhost:5001/api/generate-offer
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ offer-letter-generator/app.py - api_generate_offer()       │
│ 1. Validate input parameters                               │
│ 2. Call generate_offer_pdf()                               │
│ 3. Generate PDF with all details                           │
│ 4. Return reference number and base64 PDF                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
                PDF stored in generated/ folder
           Offer letter successfully generated
```

## Testing Steps

### 1. Start Both Services

```bash
# Terminal 1: Admin App
python admin_app.py  # Runs on port 5000

# Terminal 2: Offer Letter Generator
cd offer-letter-generator
python app.py  # Runs on port 5001
```

### 2. Accept a Candidate

1. Go to Admin Dashboard → Approved Candidates
2. Click "Accept" on any candidate
3. Choose to change domain (optional) or keep current
4. Select internship type from dropdown
5. Verify offer letter is generated (check console for success message)

### 3. Verify Data in Database

```sql
-- Check Selected table for new record
SELECT candidate_id, name, usn, role, mode_of_internship
FROM Selected
WHERE usn = '<test_usn>'
ORDER BY approved_date DESC LIMIT 1;

-- Should show:
-- candidate_id: SIN25FD001 (example)
-- mode_of_internship: remote-based opportunity (or selected type)
```

### 4. Check Generated PDF

- Offer letters stored in: `offer-letter-generator/generated/`
- Filename format: `SZS_OFFR_2025_NOV_001.pdf`

## Error Handling

### If Offer Letter Generator Not Running

- Admin app logs: "Could not connect to offer-letter-generator service on localhost:5001"
- Candidate still accepted and moved to Selected table
- Offer letter generation can be retried later

### If Offer Letter Generation Fails

- Admin app logs the error
- Candidate still accepted (not dependent on PDF generation)
- Data stored in Selected table with all information intact

## Configuration

### Port Settings

- Admin App: `http://localhost:5000` (default)
- Offer Letter Generator: `http://localhost:5001` (default)

### To Change Offer Letter Generator Port

Edit `admin_app.py` line ~1390:

```python
response = requests.post(
    'http://localhost:YOUR_PORT/api/generate-offer',  # Change port here
    json=offer_letter_data,
    timeout=30
)
```

### To Change Admin App Port

Set environment variable or modify Flask run configuration

## File Changes Summary

### Modified Files

1. **templates/admin_approved_candidates.html**

   - Added internship type modal
   - Updated JavaScript functions for modal flow
   - Added event handlers for type selection

2. **admin_app.py**

   - Modified `handle_approved_candidate_accept()` function
   - Updated `admin_accept()` route
   - Added offer letter API call with error handling
   - Fixed role storage to use full "Intern" word

3. **offer-letter-generator/app.py**
   - Refactored to extract `generate_offer_pdf()` function
   - Added new `/api/generate-offer` endpoint
   - Enhanced error handling
   - Added base64 PDF encoding for API responses

## Role Storage Fix

### Before

Could store roles as "int" (truncated) in some cases

### After

Roles are always stored as "{domain} Intern" format:

- "FULL STACK DEVELOPER Intern" ✓
- "ARTIFICIAL INTELLIGENCE Intern" ✓
- "DATA SCIENCE Intern" ✓
- etc.

## Next Steps (Optional Enhancements)

1. **Email Integration**: Send generated PDF to candidate automatically
2. **PDF Storage**: Store PDF reference in Selected table for future access
3. **Batch Processing**: Generate offer letters for multiple candidates
4. **PDF Signing**: Add digital signature to PDFs
5. **Template Customization**: Allow custom offer letter templates per domain

## Support

If offer letters are not generating:

1. Check that offer-letter-generator service is running on port 5001
2. Check admin_app logs for connection errors
3. Verify candidate data has all required fields (name, usn, college, email, role)
4. Check offer-letter-generator/generated/ folder for PDF files

---

**Implementation Date**: November 18, 2025
**Status**: Complete and Ready for Testing
