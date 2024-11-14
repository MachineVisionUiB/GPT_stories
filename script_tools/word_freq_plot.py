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

# Function to create comparative horizontal bar plots for each source with annotations
def plot_word_frequencies(combined_df, top_n=10):
    # Sort by frequency and get the top N words from each source
    top_words = combined_df.groupby('Source').apply(lambda x: x.nlargest(top_n, 'Frequency')).reset_index(drop=True)
    
    # Set up the subplot grid (2 rows, 2 columns)
    sources = top_words['Source'].unique()
    n_sources = len(sources)
    n_cols = 2
    n_rows = (n_sources + n_cols - 1) // n_cols  # Calculate number of rows needed
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(10, 5 * n_rows), sharey=True)
    
    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    for ax, source in zip(axes, sources):
        source_data = top_words[top_words['Source'] == source]
        bars = ax.barh(source_data['Word'], source_data['Frequency'], color='skyblue', alpha=0.7)
        ax.set_title(source)
        ax.set_xlabel('Frequency')

        # Add annotations next to each bar
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.2, bar.get_y() + bar.get_height()/2, int(width), 
                    va='center', ha='left', fontsize=10, color='black')

    # Hide any unused subplots
    for ax in axes[len(sources):]:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('word_frequencies_barplot.png')
    plt.show()

# Example usage
csv_files = [
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/1500w/word_freq/indian_word_frequency.csv',
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/1500w/word_freq/jpn_word_frequency.csv',
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/1500w/word_freq/nor_word_frequency.csv',
    '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/1500w/word_freq/us_word_frequency.csv'
]  # Add your CSV filenames here
combined_df = load_word_frequency_csvs(csv_files)
plot_word_frequencies(combined_df, top_n=10)