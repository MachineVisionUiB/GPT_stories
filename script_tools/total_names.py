import pandas as pd

# Load the Excel file
file_path = '/Users/hermannwigers/Downloads/10467_20241002-102356.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path, sheet_name='Personer')

# Clean the dataframe: remove unnecessary rows and columns, and focus on names and birth counts
df_clean = df.iloc[2:, 1:]  # Drop rows before index 2 and the first column (Unnamed: 0)

# Rename the columns for clarity: first column is 'Name' and the rest are the years
df_clean.columns = ['Name'] + list(range(2010, 2024))

# Replace '.' and '..' with 0
df_clean.replace({'.': 0, '..': 0}, inplace=True)

# Convert all count columns to numeric
df_clean.iloc[:, 1:] = df_clean.iloc[:, 1:].apply(pd.to_numeric)

# Sum all the years for each name
df_clean['Total'] = df_clean.iloc[:, 1:].sum(axis=1)

# Select only the 'Name' and 'Total' columns
result_df = df_clean[['Name', 'Total']]

# Filter out rows with no name
result_df = result_df[result_df['Name'].notna()]

# Save the result to a new Excel file
output_file_path = 'nor_names_female.xlsx'  # Replace with desired output file path
result_df.to_excel(output_file_path, index=False)

print(f"Processed data saved to {output_file_path}")
