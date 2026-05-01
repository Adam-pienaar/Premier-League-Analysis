#Reads the comined sheet in the excel file. Then cleans the data and completes additional information, to then create and save a cleaned CSV file.


import pandas as pd
import numpy as np
import os   

EXCEL_PATH = 'Data/PL_Finances_vs_Performance.xlsx'
OUTPUT_DIR = 'Data/processed'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'cleaned_data.csv')

def load_data():
    print("Loading data from Excel combined sheet...")
    df = pd.read_excel(EXCEL_PATH, sheet_name='combined')
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df

def clean_data(df):
    print("Cleaning and additional information...")
    # Rename columns for clarity
    df.columns = ['Club', 'League Position', 'Final Points', 'Goals Scored', 'Goals Conceded', 'Wage Cost 000s', 'Revenue 000s']
    # Convert £'000s to £m
    df['Wage Cost £m'] = df['Wage Cost 000s'] / 1000
    df['Revenue £m'] = df['Revenue 000s'] / 1000
    #calculate wage to revenue ratio
    df['Wage to Revenue Ratio'] = (df['Wage Cost £m'] / df['Revenue £m']) * 100
    # Log Revenue - to handle wide range of values and potential outliers
    df['Log Revenue'] = np.log(df['Revenue £m'])
    # Log Wage Cost - to handle wide range of values and potential outliers
    df['Log Wage Cost'] = np.log(df['Wage Cost £m'])
    # Drop the original '000s columns as they are no longer needed
    df = df.drop(columns=['Wage Cost 000s', 'Revenue 000s'])
    return df

def validate_data(df):
    print("Validating cleaned data...")
    assert len(df) == 20, f"Expected 20 clubs, got {len(df)}"
    assert df['League Position'].between(1, 100).all(), "League Position should be between 1 and 100"
    assert (df['Final Points'].between(1, 100).all()), "Final Points should be between 1 and 100"
    assert (df['Goals Scored'].gt(0).all()), "Goals Scored should be greater than 0"
    assert (df['Goals Conceded'].gt(0).all()), "Goals Conceded should be greater than 0"
    assert (df['Wage Cost £m'].gt(0).all()), "Wage Cost should be greater than 0"
    assert (df['Revenue £m'].gt(0).all()), "Revenue should be greater than 0"
    assert (df['Wage to Revenue Ratio'].between(0, 200).all()), "Wage to Revenue Ratio should be between 0 and 200%"
    assert (df['Club'].nunique() == 20), "Duplicate Club names found"
    print(" All validation checks passed.")

def save_data(df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned data saved to {OUTPUT_PATH}")

    def preview(df):
        print("/nCleaned dataset preview:")
        print(f"{'Club': <30} {'Pos': <5} {'Pts': <5} {'GF': <5} {'GA': <5} {'Wage £m': <12} {'Revenue £m': <10} {'Wage/Revenue %': <8}")
        print("-" * 85)
        for _, row in df.iterrows():
            print(f"{row['Club']: <30} {int(row['League Position']): <5} {int(row['Final Points']):<5} "
                  f"{int(row['Goals Scored']): <5} {int(row['Goals Conceded']): <5} "
                  f"{row['Wage Cost £m']: <12.3f} {row['Revenue £m']:<10.3f} {row['Wage to Revenue Ratio']:<8.1f}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    df = load_data()
    df = clean_data(df)
    validate_data(df)
    save_data(df)
    preview(df)