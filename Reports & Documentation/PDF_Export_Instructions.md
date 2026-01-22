# PDF Export Instructions

## Step 1: Run Cells in Notebook to Generate Images

1. Open `Hotel_Booking.ipynb`
2. Scroll to the **"Export Graphs for Report"** section at the bottom
3. Run all cells in that section to generate images
4. This will create a `report_images` folder with all 6 charts

## Step 2: Convert Report to PDF

### Option A: Using VS Code Extension (Recommended)
1. Install extension: "Markdown PDF" by yzane
2. Open `Hotel_Booking_Report.md`
3. Right-click → "Markdown PDF: Export (pdf)"
4. PDF will be saved in the same folder

### Option B: Using Python (If you have markdown libraries)
```bash
pip install markdown2 pdfkit
```

Then run:
```python
import pdfkit

pdfkit.from_file('Hotel_Booking_Report.md', 'Hotel_Booking_Report.pdf')
```

### Option C: Online Converter
1. Visit: https://www.markdowntopdf.com/
2. Upload `Hotel_Booking_Report.md`
3. Make sure to upload the `report_images` folder as well
4. Download the PDF

### Option D: Using Pandoc (Professional Quality)
```bash
# Install pandoc first: https://pandoc.org/installing.html

# Then run:
pandoc Hotel_Booking_Report.md -o Hotel_Booking_Report.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

## Step 3: Verify

Open the PDF and check that all 6 graphs are displaying:
- ✅ Cancellation Distribution Bar Chart
- ✅ Hotel Type Comparison
- ✅ Average Daily Rate Trends (3 years)
- ✅ Monthly Cancellations
- ✅ Top Countries Pie Chart
- ✅ ADR Cancelled vs Not Cancelled

## Troubleshooting

**If images don't show:**
1. Make sure you ran all export cells in the notebook
2. Check that `report_images` folder exists with 6 PNG files
3. Ensure the report and images folder are in the same directory

**For best results:**
- Use Option A (VS Code Extension) - easiest and most reliable
- Or Option D (Pandoc) - most professional looking
