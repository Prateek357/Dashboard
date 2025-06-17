import pandas as pd

file_path = "EUS devices.xlsx"

try:
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    print("Columns in DataFrame:", df.columns.tolist())
    if 'Primary Capability' in df.columns:
        print("Sample values in 'Primary Capability':")
        print(df['Primary Capability'].dropna().head(10).tolist())
    elif 'Primary' in df.columns:
        print("Sample values in 'Primary':")
        print(df['Primary'].dropna().head(10).tolist())
    else:
        print("Neither 'Primary Capability' nor 'Primary' column found in the DataFrame.")
except Exception as e:
    print(f"Error reading Excel file: {e}")
