import pandas as pd
import matplotlib.pyplot as plt
import os

# Specify the directory containing your CSV files
directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/noun_phrases_50words'  # Replace with your directory path

# Create a list to hold the paths of CSV files
csv_files = [f for f in os.listdir(directory) if f.endswith('_noun_phrases_output_modified.csv')]

# Create a figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()  # Flatten the axes array for easy indexing

# Loop through each file
for i, csv_file in enumerate(csv_files):
    # Load the CSV file
    file_path = os.path.join(directory, csv_file)
    df = pd.read_csv(file_path)
    
    # Get the top 10 noun phrases
    top_noun_phrases = df.nlargest(10, 'Count')  # Adjust 'Count' if the column name is different

    # Create a bar plot for the top noun phrases
    axes[i].barh(top_noun_phrases['Noun Phrase'], top_noun_phrases['Count'], color='skyblue')
    axes[i].set_title(f'Top 10 Noun Phrases from {csv_file}')
    axes[i].set_xlabel('Count')
    axes[i].invert_yaxis()  # Invert y-axis to have the highest count on top

# Adjust layout
plt.tight_layout()

# Save the figure to a file or show it
plt.savefig('top_noun_phrases_plots_modified.png')  # Saves the figure as a PNG file
# plt.show()  # Uncomment this line to display the plots instead of saving

print("Plots have been saved as 'top_noun_phrases_plots.png'")
