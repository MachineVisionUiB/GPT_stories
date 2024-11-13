import pandas as pd
from textblob import TextBlob
from collections import Counter
import os

def extract_noun_phrases(file):
    """
    Extracts and counts noun phrases from a specified column in a CSV file, then saves the results to a new CSV file.

    This function reads a CSV file, extracts text data from a specific column, and uses TextBlob to identify and count noun phrases. 
    The noun phrases are then sorted by frequency, and the results are saved to a new CSV file.

    Parameters
    ----------
    file : str
        Path to the input CSV file containing text data for noun phrase extraction.

    Raises
    ------
    IOError
        If there is an issue reading from `file` or writing to the output file.
    IndexError
        If the specified column index for text data does not exist in the file.

    Notes
    -----
    The function expects the text data to be in the fifth column (index 4) of the CSV file. Adjust the column index 
    if necessary to match your data structure.

    Examples
    --------
    >>> extract_noun_phrases('input.csv')
    This will read 'input.csv', extract and count noun phrases, and save results to 'noun_phrases_input.csv'.
    """
    df = pd.read_csv(file)
    # Extract stories from the second column
    stories = df.iloc[:, 4].tolist()  # Adjust if the column index is different. df.iloc[:, x] where x is the column index

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
    output_file = 'noun_phrases_' +  os.path.basename(os.path.normpath(file))  # Replace with your desired output file path
    output_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/summaries'
    for filename in os.listdir(directory):
        print(filename)
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            extract_noun_phrases(f)
