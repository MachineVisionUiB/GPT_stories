import pandas as pd
from textblob import TextBlob
from collections import Counter
import os

def extract_noun_phrases(dir):
    """
    Extract and count multi-word noun phrases (containing a space) from a specified 
    column in a CSV file and save the counts to a new CSV file.

    Args:
        file (str): The path to the input CSV file containing text data.

    Returns:
        pd.DataFrame: DataFrame containing filtered noun phrases and their counts.
    """

    filepath = f'../test_data/{dir}/{dir}_stories.csv'
    print(f'\nExtracting noun phrases from {filepath}...\n')
    
    df = pd.read_csv(filepath)
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

    # Location and name of output file
    output_filepath = f'../test_data/{dir}/{dir}_noun_phrases.csv'
    output_df.to_csv(output_filepath, index=False)

    




def main(countries, startfrom):
    """
    Process all CSV files in the specified directory to extract multi-word noun phrases,
    count their occurrences, and save each result to a new CSV file.
    """
    
    if 'all' in countries and len(countries) == 1:
        for dir in sorted(os.listdir("../test_data")):
            if startfrom != "" and startfrom != dir:
                continue
            else:
                startfrom = ""
                extract_noun_phrases(dir)
    else:
        for dir in sorted(os.listdir("../test_data")):
            if dir in countries:
                extract_noun_phrases(dir)

                
        


if __name__ == "__main__":
    main()
