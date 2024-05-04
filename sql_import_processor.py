import pandas as pd

# Load your template file
excel_file = 'EAP_data_real.xlsx'

# Load Excel file
xls = pd.ExcelFile(excel_file)

# Region specification for CSV naming
region_name = 'EAP'

# Iterate over each sheet in the Excel file (designed to work with unaltered template)
i = 0
for sheet_name in xls.sheet_names:
    i += 1
    if i == 6:
        break
    # Read into DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    if i != 5:
        subset_df = df.iloc[2:, 2:]
    if i == 1:
        subset_df.columns = ['Region', 'Institution', 'Type', 'Country', 'State', 'City',
                             'Design', 'Manufacturing', 'Application', 'Basic Research']
        columns_to_check = ['Institution']
    elif i ==2:
        subset_df.columns = ['SubInstName', 'InstName', 'State/Province', 'City', 'Primary Contact Name',
                             'Primary Contact Email', 'Primary Contact Website']
        columns_to_check = ['SubInstName']
    elif i == 3:
        subset_df.columns = ['RFName', 'R&D Capability', 'InstName', 'SubInstName']
        columns_to_check = ['RFName']
    elif i == 4:
        subset_df = df.iloc[2:, 1:6]
        subset_df.columns = ['Institution', 'DonatingInst', 'Collaboration Type', 'Funding Amount', 'Currency']
        columns_to_check = ['Institution', 'DonatingInst']
    elif i == 5:
        subset_df = df.iloc[2:, 1:]
        subset_df.columns = ['InstName', 'Research Area']
        columns_to_check = ['InstName', 'Research Area']
    nan_rows = subset_df[columns_to_check].isna().any(axis=1)

    # Check for NaN
    if nan_rows.any():
        first_nan_index = nan_rows[nan_rows].index[0]
        # Slice the DataFrame to keep only rows before the first NaN index (handles EOF)
        subset_df = subset_df.iloc[:first_nan_index]
    if len(subset_df) > 3:
        val = subset_df.iloc[-2, 1]
        print(val)
        if pd.isna(val):
            subset_df = subset_df.iloc[:-2, :]
    print(subset_df)
    csv_file = f'{region_name}_{i}.csv'

    subset_df.to_csv(csv_file, index=False)

