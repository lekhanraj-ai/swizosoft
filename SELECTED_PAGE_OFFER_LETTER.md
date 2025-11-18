# Selected Candidates Page - Offer Letter Viewing ✅

## Changes Made

### 1. Updated Table Structure

Added new column **"Offer Letter"** to the selected candidates table with:

- **Download Button** (📄 Download) - Downloads the stored PDF to the user's computer
- **View Button** (👁️ View) - Opens the PDF in a new browser tab for viewing
- Shows "-" if no offer letter has been generated yet

### 2. Table Column Order

```
Name | Candidate ID | USN | Roles | Approved Date | Completion Date | Offer Letter | Profile | Action
```

### 3. Functionality Added

#### Download Offer Letter

- Endpoint: `GET /admin/api/download-offer-letter/<usn>`
- Retrieves the stored PDF from database
- Downloads directly to user's Downloads folder
- Function: `downloadOfferLetter(usn)`

#### View Offer Letter

- Endpoint: `GET /admin/api/download-offer-letter/<usn>`
- Opens PDF in new browser tab
- Allows inline viewing without downloading
- Function: `viewOfferLetter(usn)`

### 4. Data Requirements

The buttons only appear if the candidate has:

- `offer_letter_reference` in the database (e.g., "SZS/OFFR/2025/NOV/005")
- `offer_letter_pdf` stored as LONGBLOB

### 5. User Interface

```
Selected Candidates Table
┌─────────────────────────────────────────────────────────────────────────┐
│ Name  │ ID   │ USN    │ Roles      │ Approved │ Completion │ Offer     │
├───────┼──────┼────────┼────────────┼──────────┼────────────┼───────────┤
│ John  │ S001 │ 4CB23  │ AI Intern  │ Nov 18   │ Feb 18     │ 📄 ▲ 👁️ ▲ │
│ Jane  │ S002 │ 4CB24  │ DS Intern  │ Nov 17   │ Feb 17     │     -      │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6. Database Integration

The feature reads from Selected table:

- `offer_letter_reference` - Determines if offer exists
- `offer_letter_pdf` - The actual PDF binary data (LONGBLOB)

### 7. Status Display

- ✅ **Offer Letter with buttons** - If `offer_letter_reference` exists
- ⚠️ **"-" dash** - If no offer letter generated yet

## How It Works

1. Admin/user navigates to **"Selected Candidates"** page
2. Table loads with all selected candidates
3. For each candidate with an offer letter:
   - Shows **"📄 Download"** button - to save PDF locally
   - Shows **"👁️ View"** button - to view in browser
4. Click buttons to download or view the offer letter

## Files Modified

- `templates/admin_selected.html` - Added offer letter column and buttons

## Workflow Integration

```
Approved Candidates Page
        ↓
    Accept + Select Internship Type
        ↓
    Data stored in Selected table
        ↓
    Generate Offer Letter
        ↓
    PDF stored in database (offer_letter_pdf)
        ↓
    Selected Candidates Page
        ↓
    📄 Download or 👁️ View Offer Letter ✅ (NEW)
```

## Testing the Feature

1. Navigate to admin dashboard
2. Go to "Selected Candidates" page
3. For candidates with stored offers, buttons appear in "Offer Letter" column
4. Click "📄 Download" to download PDF
5. Click "👁️ View" to open in new tab

## API Endpoints Used

**GET /admin/api/download-offer-letter/<usn>**

- Returns: PDF file (binary)
- Uses: `send_file()` with Flask
- Database: Retrieves from Selected.offer_letter_pdf column
