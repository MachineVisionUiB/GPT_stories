import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/hf_sentiment_count_85.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Drop rows with NaN values in 'Sentiment' and 'Count'
cleaned_data = data.dropna(subset=['Sentiment', 'Count'])
cleaned_data['Count'] = cleaned_data['Count'].astype(int)

# Get unique file names
unique_files = cleaned_data['File Name'].dropna().unique()

# Set up the number of rows and columns for subplots
num_files = len(unique_files)
fig, axes = plt.subplots(num_files, 1, figsize=(10, 6 * num_files), constrained_layout=True)

# Plot each file's data in a separate subplot
for i, file_name in enumerate(unique_files):
    file_data = cleaned_data[cleaned_data['File Name'] == file_name]
    sns.barplot(ax=axes[i], x='Sentiment', y='Count', data=file_data, palette='viridis')
    
    # Title and labels for each subplot
    axes[i].set_title(f'Sentiment Counts for {file_name}')
    axes[i].set_xlabel('Sentiment')
    axes[i].set_ylabel('Count')

# Display the combined plot
plt.show()
