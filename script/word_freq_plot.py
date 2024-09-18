import pandas as pd
import matplotlib.pyplot as plt
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

# Function to create a comparative bar plot
def plot_word_frequencies(combined_df, top_n=10):
    # Sort by frequency and get the top N words from each source
    top_words = combined_df.groupby('Source').apply(lambda x: x.nlargest(top_n, 'Frequency')).reset_index(drop=True)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    for source in top_words['Source'].unique():
        source_data = top_words[top_words['Source'] == source]
        plt.bar(source_data['Word'], source_data['Frequency'], label=source, alpha=0.7)
    
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Word Frequencies Comparison')
    plt.legend(title='Source')
    plt.tight_layout()
    plt.show()

# Example usage
csv_files = ['/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/american_stories_word_frequency.csv', '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/norwegian_stories_word_frequency.csv',
             '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/persian_stories_word_frequency.csv', '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/word_freq/100_words/japanese_stories_word_frequency.csv']  # Add your CSV filenames here
combined_df = load_word_frequency_csvs(csv_files)
plot_word_frequencies(combined_df, top_n=10)
