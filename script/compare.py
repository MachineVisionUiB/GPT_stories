import pandas as pd

# Load the two CSV files
df1 = pd.read_csv('path_to_output_file.csv')
df2 = pd.read_csv('name_frequencies_australian.csv')

# Strip any leading/trailing spaces from column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Merge the two DataFrames on the 'Name' column using outer join to include all names
merged_df = pd.merge(df1, df2, on='Name', how='outer')

# Rename columns for clarity
merged_df.rename(columns={'Frequency_x': 'Frequency1', 'Frequency_y': 'Frequency2'}, inplace=True)

# Sort the merged DataFrame by the 'Frequency2' column in descending order
merged_df = merged_df.sort_values(by=merged_df.columns[2], ascending=False)

# Select only the 'Name', 'Frequency1', and 'Frequency2' columns
merged_df = merged_df[['Name', 'Frequency1', 'Frequency2']]

# Print the merged DataFrame
print(merged_df)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_frequencies.csv', index=False)

print("Merged CSV file saved successfully.")
