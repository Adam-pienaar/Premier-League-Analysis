# Premier-League-Analysis
## Terminal Setup & Troubleshooting

### 1. Initialising Git and Connecting to GitHub
```bash
git init
git remote add origin https://github.com/Adam-pienaar/Premier-League-Analysis.git
git pull origin main
```

### 2. Troubleshooting: Untracked Files Error
When pulling from GitHub, the following error occurred because local files already existed: error: The following untracked working tree files would be overwritten by merge:
Data/PL_Finances_vs_Performance.xlsx
README.md
Please move or remove them before you merge.
Aborting
**Fix:** Back up the local script and force sync with GitHub:
```bash
cp scripts/clean_data.py ~/Desktop/clean_data.py
git fetch origin
git reset --hard origin/main
cp ~/Desktop/clean_data.py scripts/clean_data.py
```

### 3. Pushing to GitHub
```bash
git add .
git commit -m "Add data cleaning script"
git push origin main
```

### 4. Troubleshooting: Permission Denied (403 Error)
GitHub rejected the push because the wrong account was being used: remote: Permission to Adam-pienaar/Premier-League-Analysis.git denied to pienaar2004-source.
fatal: unable to access '...': The requested URL returned error: 403
**Fix:** Update the remote URL to use the correct account and personal access token:
```bash
git remote set-url origin https://Adam-pienaar@github.com/Adam-pienaar/Premier-League-Analysis.git
git push origin main
```

### 5. Troubleshooting: FileNotFoundError Running the Script
The script couldn't find the Excel file due to a case mismatch (`vs` vs `VS`) in the filename: FileNotFoundError: [Errno 2] No such file or directory: 'Data/PL_Finances_vs_Performance.xlsx'
**Fix:** Updated the file path in `clean_data.py` to match the exact filename:
```python
EXCEL_PATH = 'Data/PL_Finances_VS_Performance.xlsx'
```

### 6. Running the Cleaning Script Successfully
```bash
python Scripts/clean_data.py
```
**Output:**
Loading data from Excel combined sheet...
Loaded 20 rows and 7 columns.
Cleaning and additional information...
Validating cleaned data...
All validation checks passed.
Cleaned data saved to Data/processed/cleaned_data.csv

