import pandas as pd

# Load the two CSV files
df1 = pd.read_csv('/Users/hermannwigers/Documents/AI STORIES/GPT_stories/nor_name_frequencies_f.csv')
df2 = pd.read_excel('/Users/hermannwigers/Documents/AI STORIES/GPT_stories/nor_names_female.xlsx')

# Strip any leading/trailing spaces from column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Merge the two DataFrames on the 'Name' column using outer join to include all names
merged_df = pd.merge(df1, df2, on='Name', how='outer')

# Rename columns for clarity
merged_df.rename(columns={'Frequency': 'story', 'Total': 'dataset'}, inplace=True)

# Step 2: Convert floats to ints and NaN to 0 for 'story' and 'dataset' columns
merged_df['story'] = merged_df['story'].fillna(0).astype(int)  # Replace NaN with 0 and convert to int
merged_df['dataset'] = merged_df['dataset'].fillna(0).astype(int)  # Same for dataset

# Step 3: Sort the DataFrame based on the 'story' column
df_sorted = merged_df.sort_values(by="story", ascending=False)  # Ensure sorting by 'story'

# Select only the 'Name', 'story', and 'dataset' columns
final_df = df_sorted[['Name', 'story', 'dataset']]  # Use the sorted DataFrame

# Print the sorted DataFrame
print(final_df)

# Get output file name from user
output_file = input("Enter the output file name: ") + "_merged_name_frequencies" + '.csv'
# Save the merged DataFrame to a new CSV file
final_df.to_csv(output_file, index=False)

print("Merged CSV file saved successfully.")
