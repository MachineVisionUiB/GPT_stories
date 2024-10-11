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
    top_words = combined_df.groupby('Source').apply(lambda x: x.nlargest(top_n, 'Frequency')).reset_index(drop=True)
    
    # Pivot the DataFrame to create a matrix for the heatmap
    heatmap_data = top_words.pivot(index='Word', columns='Source', values='Frequency').fillna(0)
    
    # Create the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='Blues', cbar_kws={'label': 'Frequency'})
    plt.title(f'Top {top_n} Word Frequencies Heatmap')
    plt.xlabel('Source')
    plt.ylabel('Words')
    plt.tight_layout()
    plt.savefig('word_frequencies_heatmap.png')
    plt.show()

# Example usage
csv_files = [
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/american_stories_word_frequency.csv',
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/norwegian_stories_word_frequency.csv',
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/persian_stories_word_frequency.csv',
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/japanese_stories_word_frequency.csv'
]  # Add your CSV filenames here
combined_df = load_word_frequency_csvs(csv_files)
plot_word_frequencies_heatmap(combined_df, top_n=10)

