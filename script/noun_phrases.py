import pandas as pd
from textblob import TextBlob
from collections import Counter
import os

def extract_noun_phrases(file):
    """
    Extract and count noun phrases from a specified column in a CSV file
    and save the counts to a new CSV file.

    This function reads a CSV file, extracts text from a specified column,
    and uses TextBlob to identify noun phrases. It counts occurrences of each
    noun phrase and writes the results to a new CSV file in descending order
    of frequency.

    Args:
        file (str): The path to the input CSV file containing text data.

    Example:
        file = '/path/to/input.csv'
        extract_noun_phrases(file)
    """
    
    df = pd.read_csv(file)
    # Extract stories from the fifth column
    stories = df.iloc[:, 4].tolist()  # Adjust if the column index is different

    # Extract noun phrases
    noun_phrases = []
    for story in stories:
        blob = TextBlob(story)
        noun_phrases.extend(blob.noun_phrases)

    # Count and sort noun phrases
    noun_phrase_counts = Counter(noun_phrases)
    sorted_noun_phrases = noun_phrase_counts.most_common()

    # Create a DataFrame for the output
    output_df = pd.DataFrame(sorted_noun_phrases, columns=['Noun Phrase', 'Count'])

    # Save to a new CSV file
    output_file = 'noun_phrases_' + os.path.basename(os.path.normpath(file))  # Replace with your desired output file path
    output_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    """
    Process all CSV files in the specified directory to extract noun phrases,
    count their occurrences, and save each result to a new CSV file.
    """
    
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/summaries'
    for filename in os.listdir(directory):
        print(filename)
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            extract_noun_phrases(f)
