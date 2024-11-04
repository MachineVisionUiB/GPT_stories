import pandas as pd

# Step 1: Load the CSV file
file_path = 'your_file.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Step 2: Convert floats to ints and NaN to 0
df['story'] = df['story'].fillna(0).astype(int)  # Replace NaN with 0 and convert to int
df['dataset'] = df['dataset'].fillna(0).astype(int)  # Same for dataset

# Step 3: Sort the DataFrame based on the 'story' column
df_sorted = df.sort_values(by='story')

# Step 4: Save the modified DataFrame to a new CSV file
df_sorted.to_csv('modified_file.csv', index=False)  # Replace with desired output file path
