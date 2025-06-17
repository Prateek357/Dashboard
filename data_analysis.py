import pandas as pd

import pandas as pd
from datetime import datetime

def main():
    # Load the Excel file into a DataFrame
    file_path = "EUS devices.xlsx"
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return

    # Filter rows by Status
    status_filter = ["Deployed", "Deployed - Work from Home", "Stand Alone"]
    df_filtered = df[df['Status'].isin(status_filter)]

    # Get current date for comparison
    today = pd.to_datetime(datetime.now().date())

    # Helper function to check if current date is within start and end date range
    def is_currently_covered(start_date, end_date):
        if pd.isna(start_date) or pd.isna(end_date):
            return False
        return (start_date <= today) and (today <= end_date)

    # Categorize devices based on Warranty, AMC, and Insurance coverage
    df_filtered['In Warranty'] = df_filtered.apply(
        lambda row: is_currently_covered(row['Warranty Start Date'], row['Warranty End Date']), axis=1)
    df_filtered['In AMC'] = df_filtered.apply(
        lambda row: is_currently_covered(row['AMC Start Date'], row['AMC End Date']), axis=1)
    df_filtered['In Insurance'] = df_filtered.apply(
        lambda row: is_currently_covered(row['Insurance Start Date'], row['Insurance End Date']), axis=1)

    # Devices in Warranty with or without Insurance
    warranty_with_insurance = df_filtered[(df_filtered['In Warranty']) & (df_filtered['In Insurance'])]
    warranty_without_insurance = df_filtered[(df_filtered['In Warranty']) & (~df_filtered['In Insurance'])]

    # Devices in AMC with or without Insurance
    amc_with_insurance = df_filtered[(df_filtered['In AMC']) & (df_filtered['In Insurance'])]
    amc_without_insurance = df_filtered[(df_filtered['In AMC']) & (~df_filtered['In Insurance'])]

    # Print summary counts
    print("Summary of device categorization based on Warranty, AMC, and Insurance coverage:")
    print(f"Devices in Warranty with Insurance: {len(warranty_with_insurance)}")
    print(f"Devices in Warranty without Insurance: {len(warranty_without_insurance)}")
    print(f"Devices in AMC with Insurance: {len(amc_with_insurance)}")
    print(f"Devices in AMC without Insurance: {len(amc_without_insurance)}")
    print("\n")

    # Optionally, print first few rows of each category
    print("Sample devices in Warranty with Insurance:")
    print(warranty_with_insurance[['CI ID', 'CI Name', 'Status', 'Warranty Start Date', 'Warranty End Date', 'Insurance Start Date', 'Insurance End Date']].head())
    print("\n")

    print("Sample devices in Warranty without Insurance:")
    print(warranty_without_insurance[['CI ID', 'CI Name', 'Status', 'Warranty Start Date', 'Warranty End Date']].head())
    print("\n")

    print("Sample devices in AMC with Insurance:")
    print(amc_with_insurance[['CI ID', 'CI Name', 'Status', 'AMC Start Date', 'AMC End Date', 'Insurance Start Date', 'Insurance End Date']].head())
    print("\n")

    print("Sample devices in AMC without Insurance:")
    print(amc_without_insurance[['CI ID', 'CI Name', 'Status', 'AMC Start Date', 'AMC End Date']].head())
    print("\n")

if __name__ == "__main__":
    main()
