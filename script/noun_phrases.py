import pandas as pd
from textblob import TextBlob
from collections import Counter
import os

def extract_noun_phrases(file):
    """
    Extract and count multi-word noun phrases (containing a space) from a specified 
    column in a CSV file and save the counts to a new CSV file.

    Args:
        file (str): The path to the input CSV file containing text data.

    Returns:
        pd.DataFrame: DataFrame containing filtered noun phrases and their counts.
    """
    
    df = pd.read_csv(file)
    # Extract stories from the fifth column
    stories = df.iloc[:, 4].tolist()  # Adjust if the column index is different

    # Extract noun phrases 
    noun_phrases = []
    for story in stories:
        blob = TextBlob(story)
        noun_phrases.extend(blob.noun_phrases)

    # Filter noun phrases to include only those with a space
    multi_word_phrases = [phrase for phrase in noun_phrases if ' ' in phrase]

    # Count and sort noun phrases
    noun_phrase_counts = Counter(multi_word_phrases)
    sorted_noun_phrases = noun_phrase_counts.most_common()

    # Create a DataFrame for the output
    output_df = pd.DataFrame(sorted_noun_phrases, columns=['Noun Phrase', 'Count'])

    return output_df


def main():
    """
    Process all CSV files in the specified directory to extract multi-word noun phrases,
    count their occurrences, and save each result to a new CSV file.
    """
    
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/summaries'
    for filename in os.listdir(directory):
        print(filename)
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            output_df = extract_noun_phrases(f)
            # Save the output to a CSV file
            # output_file = 'filtered_noun_phrases_' + os.path.basename(f)
            # output_df.to_csv(output_file, index=False)
    
    return output_df
        


if __name__ == "__main__":
    main()
