# Quick Reference - Offer Letter Automation

## What Was Done

### Problem Addressed

1. **Roles storage issue**: Roles now properly store as "domain Intern" (with full word "intern", not "int")
2. **Manual offer letter generation**: Automated via APIs
3. **Missing internship type selection**: Added modal for admin to choose remote/hybrid/on-site
4. **Domain change UX**: Improved flow with sequential modals

### Solution Implemented

#### Frontend Changes

- **New Modal**: Internship Type Selection Modal
- **Flow**: Accept → Domain Modal → Internship Type Modal → Auto-Generate Offer Letter
- **File**: `templates/admin_approved_candidates.html`

#### Backend Changes

- **Updated handler**: `handle_approved_candidate_accept()` now accepts `internship_type` parameter
- **New API call**: Calls offer-letter-generator with candidate data
- **Database update**: Stores `mode_of_internship` with selected type
- **File**: `admin_app.py`

#### Offer Letter Generator Changes

- **Refactored**: Created reusable `generate_offer_pdf()` function
- **New API endpoint**: `POST /api/generate-offer` for automated generation
- **Response format**: Returns JSON with base64-encoded PDF
- **File**: `offer-letter-generator/app.py`

## How It Works

```
1. Admin clicks "Accept" on candidate
   ↓
2. System shows Domain Change Modal (existing)
   ↓
3. System shows Internship Type Modal (NEW)
   ↓
4. Admin selects internship type
   ↓
5. System:
   - Accepts candidate
   - Moves to Selected table
   - Stores internship type in mode_of_internship field
   - Generates offer letter PDF
   - Returns success message
```

## Testing Checklist

- [ ] Start admin_app on port 5000
- [ ] Start offer-letter-generator on port 5001
- [ ] Go to Approved Candidates page
- [ ] Click Accept on a candidate
- [ ] Change domain (optional) in Modal 1
- [ ] Select internship type in Modal 2
- [ ] Verify:
  - [ ] Candidate moved to Selected table
  - [ ] Internship type stored correctly
  - [ ] Offer letter generated in `generated/` folder
  - [ ] No errors in admin app console

## Database Fields Updated

### Selected Table

- **mode_of_internship**: Now stores one of:
  - `'remote-based opportunity'`
  - `'hybrid-based opportunity'`
  - `'on-site based opportunity'`
  - `'free'` (backward compatible)
  - `'paid'` (backward compatible)

## API Endpoints

### New Endpoint

```
POST /api/generate-offer
Content-Type: application/json

Request Body:
{
  "name": "John Doe",
  "usn": "CS123456",
  "email": "john@example.com",
  "college": "IIIT Bangalore",
  "role": "FULL STACK DEVELOPER Intern",
  "duration": "3 months",
  "internship_type": "remote-based opportunity"
}

Response:
{
  "success": true,
  "message": "Offer letter generated successfully",
  "reference_number": "SZS/OFFR/2025/NOV/001",
  "filename": "SZS_OFFR_2025_NOV_001.pdf",
  "pdf_data": "<base64_encoded_pdf>"
}
```

## File Locations

### Modified Files

1. `templates/admin_approved_candidates.html` - Added internship type modal and JS functions
2. `admin_app.py` - Updated acceptance handler and added API call
3. `offer-letter-generator/app.py` - Refactored PDF generation and added API endpoint

### Generated Files

- Offer letters: `offer-letter-generator/generated/SZS_OFFR_YYYY_MMM_XXX.pdf`

## Troubleshooting

### Offer letter not generating?

1. Check if offer-letter-generator is running on port 5001
2. Check admin_app console for "Could not connect" message
3. Verify all required candidate fields are populated
4. Check Generated folder for PDF files

### Internship type modal not showing?

1. Clear browser cache (Ctrl+Shift+Delete)
2. Check admin_approved_candidates.html was updated
3. Reload admin dashboard page

### Wrong internship type stored?

1. Check Selected table `mode_of_internship` field
2. Verify the three offered options in modal match your requirements
3. Update modal options in HTML if needed

## Configuration

### Ports

- Admin App: 5000 (default)
- Offer Generator: 5001 (default)

To change offer generator port in admin_app.py:

```python
# Line ~1390
response = requests.post(
    'http://localhost:YOUR_PORT/api/generate-offer',  # Change port
    json=offer_letter_data,
    timeout=30
)
```

## Success Indicators

✓ Internship Type Modal appears after domain selection
✓ Admin can select remote/hybrid/on-site options
✓ Candidate moved to Selected table with correct type
✓ PDF generated in `generated/` folder
✓ No JavaScript errors in browser console
✓ No connection errors in admin_app console

---

**Implementation Status**: ✅ COMPLETE
**Last Updated**: November 18, 2025
