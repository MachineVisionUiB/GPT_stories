import pandas as pd

# Load the CSV file
df = pd.read_csv('male_and_female_top100.csv')

# Print the exact column names for debugging
print("Original df columns:", df.columns.tolist())

# Strip any leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Print the cleaned column names for debugging
print("Cleaned df columns:", df.columns.tolist())

# Check if the columns 'Given Name', 'Amount', and 'Position' exist
required_columns = ['Given Name', 'Amount', 'Position']
if all(col in df.columns for col in required_columns):
    # Keep only the 'Given Name' and 'Amount' columns
    df = df[['Given Name', 'Amount']]
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv('path_to_output_file.csv', index=False)
    
    print("Updated CSV file saved successfully.")
else:
    print(f"The required columns {required_columns} do not exist in the DataFrame.")

