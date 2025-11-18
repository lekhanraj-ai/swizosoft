# Quick Reference - Offer Letter Viewing

## Access the Feature

1. **Navigate to Selected Candidates Page**

   - URL: `http://127.0.0.1:5000/admin/selected`
   - Or click "Selected Candidates" in navigation menu

2. **Look for "Offer Letter" Column**

   - Position: Between "Completion Date" and "Profile" columns
   - Shows status for each candidate

3. **Take Action**
   - **📄 Download Button**: Save PDF to your computer
   - **👁️ View Button**: Open PDF in new browser tab
   - **"-" Dash**: No offer letter generated yet

## Database Columns

```sql
Selected table:
├─ offer_letter_pdf (LONGBLOB) -- Stores PDF file
├─ offer_letter_reference (VARCHAR 50) -- e.g., "SZS/OFFR/2025/NOV/005"
└─ offer_letter_generated_date (TIMESTAMP) -- When generated
```

## API Endpoints

```
GET /admin/api/download-offer-letter/<usn>
├─ Returns: PDF file (binary)
├─ Used by: Download and View buttons
└─ Auth: @login_required
```

## Workflow

```
Generate Offer → Stored in Database → View on Selected Page → Download or View PDF
```

## Button Functionality

| Button      | Action            | Result                 |
| ----------- | ----------------- | ---------------------- |
| 📄 Download | Click to download | PDF saves to Downloads |
| 👁️ View     | Click to view     | PDF opens in new tab   |
| "-"         | Not clickable     | No offer generated     |

## Status Indicators

- ✅ **Offer Letter with Buttons** = Stored in database, ready to use
- ⚠️ **"-" Dash** = Offer letter pending generation
- 🔄 **After Accept** = Generate offer, then buttons appear

## Testing the Feature

1. Go to Approved Candidates
2. Accept a candidate (select internship type)
3. Go to Selected Candidates
4. New candidate appears in table
5. If offer generated, see Download/View buttons
6. Click buttons to access offer

## Common Issues

**Can't see buttons?**

- Offer letter hasn't been generated yet
- Generate from approved candidates page first

**PDF won't download?**

- Check browser settings
- Try "View" button instead
- Ensure logged in

**Can't find page?**

- Click "Selected Candidates" in navbar
- Or navigate to `/admin/selected`

## Key Features

✅ Professional PDF formatting
✅ Database storage (never lost)
✅ Reference number tracking
✅ Timestamp recording
✅ One-click download/view
✅ Responsive design
✅ Secure access (login required)
