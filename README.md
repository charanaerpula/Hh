# Hh

## Overview ✅
Simple script to fetch exam results by hall ticket number range and save them as an Excel workbook (.xlsx). Excel output is the default and required.

## Requirements 🔧
- Python 3.8+ recommended
- pip

Runtime packages:
- `requests`
- `beautifulsoup4`

Required (Excel export is the default and mandatory):
- `pandas`
- `openpyxl`

Install packages:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

It is recommended to use a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Usage 🧭
Interactive (prompts):
```bash
python m.py
```
You'll be prompted in this order:
1. Enter exam URL (required)
2. Enter start hall ticket number
3. Enter end hall ticket number

To change the output filename use `--output` (defaults to `ou_results.xlsx`).

Non-interactive (flags):
```bash
python m.py --url "https://example.com/res.jsp" --start 110624861001 --end 110624861064 --output results.xlsx
```

### Result Excel format 📊
The `results` sheet is organized exactly as requested:

- Columns (in order):
  1. `hallticket` (numeric/student id)
  2. `student.name` (student full name)
  3. `student.father` (father's name)
  4. One column per **subject code** (column header = the subject code) containing the grade for that subject
  5. `result` (PASSED / PROMOTED / etc.)

Special ordering rules for subject-code columns:
- Non-lab subject codes are ordered by frequency (most common first), then split into two halves.
- All lab codes (codes containing `LAB`) are placed *between* the common and uncommon halves.
- Any remaining subject codes (not in the frequency list) are appended alphabetically.

Other sheets in the workbook:
- `grades`: Pivoted grades per code (codes as columns) — useful for quick grade lookups.
- `marks`: Long-form marks table (one row per student-per-subject with `code`, `subject`, `credits`, `grade`).
- `raw`: The original NDJSON lines, one JSON string per row.

## Convert existing JSON/NDJSON to Excel
A helper `json_to_excel.py` is included to convert result files to an Excel workbook.

Usage:
```bash
python json_to_excel.py ou_results.json results.xlsx
```

Optional: protect grades sheet:

```bash
python json_to_excel.py ou_results.ndjson ou_results.xlsx --protect-password mysecret
```

Cleaning & final files
----------------------
This repo keeps only the production scripts and the final Excel output. Test artifacts and temporary sample files (e.g., `test_sample.ndjson`, `test_sample_out.xlsx`) have been removed from the repository to avoid confusion.

Notes & requirements
--------------------
- Requires: Python 3.8+, `pandas`, `openpyxl`, `requests`, `beautifulsoup4`.

---

I added `requirements.txt` that includes the required dependencies (`requests`, `beautifulsoup4`, `pandas`, `openpyxl`).

Install dependencies:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```


