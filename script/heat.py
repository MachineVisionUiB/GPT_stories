import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Function to read multiple CSVs and combine their word frequencies
def load_word_frequency_csvs(csv_files):
    data_frames = []
    
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df['Source'] = os.path.splitext(os.path.basename(csv_file))[0]  # Add a column to indicate the source
        data_frames.append(df)
    
    # Combine all data into a single DataFrame
    combined_df = pd.concat(data_frames)
    return combined_df

# Function to create a heatmap of word frequencies
def plot_word_frequencies_heatmap(combined_df, top_n=10):
    # Get the top N words for each source
    top_words = combined_df.groupby('Source').apply(lambda x: x.nlargest(top_n, 'Frequency').head(top_n)).reset_index(drop=True)

    
    # Get all unique words from the top words across all sources
    unique_words = top_words['Word'].unique()
    
    # Filter the combined dataframe to include only the unique words
    filtered_df = combined_df[combined_df['Word'].isin(unique_words)]
    
    # Pivot the DataFrame to create a matrix for the heatmap
    heatmap_data = filtered_df.pivot(index='Word', columns='Source', values='Frequency').fillna(0)
    
    # Reorder the rows to match the most frequent words in the heatmap
    heatmap_data = heatmap_data.loc[unique_words]
    
    # Create the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='Blues', cbar_kws={'label': 'Frequency'})
    plt.title(f'Top 21 Word Frequencies Heatmap (summaries)')
    plt.xlabel('Source')
    plt.ylabel('Words')
    plt.tight_layout()
    plt.savefig('word_frequencies_heatmap_1500w_summaries.png')
    plt.show()




if __name__ == "__main__":
    # Call the analyze_stories function with the input CSV file
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/full_stories_analysis/word_freq'
    csv_files = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            csv_files.append(f)

    print(csv_files)
    combined_df = load_word_frequency_csvs(csv_files)
    plot_word_frequencies_heatmap(combined_df, top_n=10)