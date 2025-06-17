from flask import Flask, render_template, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def run_analysis():
    file_path = "EUS devices.xlsx"
    try:
        df = pd.read_excel(file_path)
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        # Debug print to verify columns
        print("Columns in DataFrame:", df.columns.tolist())
    except Exception as e:
        return {"error": f"Error loading Excel file: {e}"}
    

    status_filter = ["Deployed", "Deployed - Work from Home", "Stand Alone"]
    df_filtered = df[df['Status'].isin(status_filter)]

    today = pd.to_datetime(datetime.now().date())

    def is_currently_covered(start_date, end_date):
        if pd.isna(start_date) or pd.isna(end_date):
            return False
        return (start_date <= today) and (today <= end_date)

    df_filtered.loc[:, 'In Warranty'] = df_filtered.apply(
        lambda row: is_currently_covered(row['Warranty Start Date'], row['Warranty End Date']), axis=1)
    df_filtered.loc[:, 'In AMC'] = df_filtered.apply(
        lambda row: is_currently_covered(row['AMC Start Date'], row['AMC End Date']), axis=1)
    df_filtered.loc[:, 'In Insurance'] = df_filtered.apply(
        lambda row: is_currently_covered(row['Insurance Start Date'], row['Insurance End Date']), axis=1)

    warranty_with_insurance = df_filtered[(df_filtered['In Warranty']) & (df_filtered['In Insurance'])]
    warranty_without_insurance = df_filtered[(df_filtered['In Warranty']) & (~df_filtered['In Insurance'])]
    amc_with_insurance = df_filtered[(df_filtered['In AMC']) & (df_filtered['In Insurance'])]
    amc_without_insurance = df_filtered[(df_filtered['In AMC']) & (~df_filtered['In Insurance'])]

    # Determine the correct column name for primary capability
    primary_col = None
    for col in ['Primary Capability', 'Primary']:
        if col in df.columns:
            primary_col = col
            break
    if primary_col is None:
        return {"error": "Primary capability column not found in dataset"}

    result = {
        "summary": {
            "warranty_with_insurance": len(warranty_with_insurance),
            "warranty_without_insurance": len(warranty_without_insurance),
            "amc_with_insurance": len(amc_with_insurance),
            "amc_without_insurance": len(amc_without_insurance),
        },
        "samples": {
            "warranty_with_insurance": warranty_with_insurance[['CI ID', 'CI Name', 'Status', 'Warranty Start Date', 'Warranty End Date', 'Insurance Start Date', 'Insurance End Date']].head().to_dict(orient='records'),
            "warranty_without_insurance": warranty_without_insurance[['CI ID', 'CI Name', 'Status', 'Warranty Start Date', 'Warranty End Date']].head().to_dict(orient='records'),
            "amc_with_insurance": amc_with_insurance[['CI ID', 'CI Name', 'Status', 'AMC Start Date', 'AMC End Date', 'Insurance Start Date', 'Insurance End Date']].head().to_dict(orient='records'),
            "amc_without_insurance": amc_without_insurance[['CI ID', 'CI Name', 'Status', 'AMC Start Date', 'AMC End Date']].head().to_dict(orient='records'),
        },
        "primary_capabilities": {
            "warranty_with_insurance": warranty_with_insurance[primary_col].dropna().str.strip().replace('', pd.NA).dropna().unique().tolist(),
            "warranty_without_insurance": warranty_without_insurance[primary_col].dropna().str.strip().replace('', pd.NA).dropna().unique().tolist(),
            "amc_with_insurance": amc_with_insurance[primary_col].dropna().str.strip().replace('', pd.NA).dropna().unique().tolist(),
            "amc_without_insurance": amc_without_insurance[primary_col].dropna().str.strip().replace('', pd.NA).dropna().unique().tolist(),
        }
    }
    # Additional debug prints to verify data filtering and primary capability values
    print("Filtered DataFrame sizes:")
    print(f"Warranty with insurance: {len(warranty_with_insurance)}")
    print(f"Warranty without insurance: {len(warranty_without_insurance)}")
    print(f"AMC with insurance: {len(amc_with_insurance)}")
    print(f"AMC without insurance: {len(amc_without_insurance)}")

    print("Sample Primary Capability values:")
    print(f"Warranty with insurance: {warranty_with_insurance[primary_col].head().tolist()}")
    print(f"Warranty without insurance: {warranty_without_insurance[primary_col].head().tolist()}")
    print(f"AMC with insurance: {amc_with_insurance[primary_col].head().tolist()}")
    print(f"AMC without insurance: {amc_without_insurance[primary_col].head().tolist()}")

    print("Primary capabilities extracted:", {
        "warranty_with_insurance": result["primary_capabilities"]["warranty_with_insurance"],
        "warranty_without_insurance": result["primary_capabilities"]["warranty_without_insurance"],
        "amc_with_insurance": result["primary_capabilities"]["amc_with_insurance"],
        "amc_without_insurance": result["primary_capabilities"]["amc_without_insurance"],
    })
    return result

from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

def run_analysis():
    file_path = "EUS devices.xlsx"
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return {"error": f"Error loading Excel file: {e}"}

    status_filter = ["Deployed", "Deployed - Work from Home", "Stand Alone"]
    df_filtered = df[df['Status'].isin(status_filter)]

    today = pd.to_datetime(datetime.now().date())

    def is_currently_covered(start_date, end_date):
        if pd.isna(start_date) or pd.isna(end_date):
            return False
        return (start_date <= today) and (today <= end_date)

    df_filtered['In Warranty'] = df_filtered.apply(
        lambda row: is_currently_covered(row['Warranty Start Date'], row['Warranty End Date']), axis=1)
    df_filtered['In AMC'] = df_filtered.apply(
        lambda row: is_currently_covered(row['AMC Start Date'], row['AMC End Date']), axis=1)
    df_filtered['In Insurance'] = df_filtered.apply(
        lambda row: is_currently_covered(row['Insurance Start Date'], row['Insurance End Date']), axis=1)

    warranty_with_insurance = df_filtered[(df_filtered['In Warranty']) & (df_filtered['In Insurance'])]
    warranty_without_insurance = df_filtered[(df_filtered['In Warranty']) & (~df_filtered['In Insurance'])]
    amc_with_insurance = df_filtered[(df_filtered['In AMC']) & (df_filtered['In Insurance'])]
    amc_without_insurance = df_filtered[(df_filtered['In AMC']) & (~df_filtered['In Insurance'])]

    result = {
        "summary": {
            "warranty_with_insurance": len(warranty_with_insurance),
            "warranty_without_insurance": len(warranty_without_insurance),
            "amc_with_insurance": len(amc_with_insurance),
            "amc_without_insurance": len(amc_without_insurance),
        },
        "samples": {
            "warranty_with_insurance": warranty_with_insurance[['CI ID', 'CI Name', 'Status', 'Warranty Start Date', 'Warranty End Date', 'Insurance Start Date', 'Insurance End Date']].head().to_dict(orient='records'),
            "warranty_without_insurance": warranty_without_insurance[['CI ID', 'CI Name', 'Status', 'Warranty Start Date', 'Warranty End Date']].head().to_dict(orient='records'),
            "amc_with_insurance": amc_with_insurance[['CI ID', 'CI Name', 'Status', 'AMC Start Date', 'AMC End Date', 'Insurance Start Date', 'Insurance End Date']].head().to_dict(orient='records'),
            "amc_without_insurance": amc_without_insurance[['CI ID', 'CI Name', 'Status', 'AMC Start Date', 'AMC End Date']].head().to_dict(orient='records'),
        }
    }
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    result = run_analysis()
    if "error" in result:
        return render_template('analysis.html', error=result["error"])
    # Add primary_capabilities key if missing to avoid template error
    if "primary_capabilities" not in result:
        result["primary_capabilities"] = {
            "warranty_with_insurance": [],
            "warranty_without_insurance": [],
            "amc_with_insurance": [],
            "amc_without_insurance": []
        }
    return render_template('analysis.html', result=result)

@app.route('/run_analysis')
def run_analysis_route():
    result = run_analysis()
    return jsonify(result)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)
