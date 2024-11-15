import pandas as pd
import spacy
from collections import Counter
import os

# Load SpaCy's English language model
nlp = spacy.load('en_core_web_sm')

def lemmatize_and_count(texts):
    """
    Lemmatize words and count frequencies in a list of text entries.

    Processes a list of text entries, lemmatizing each word and counting 
    the occurrences of each unique word, excluding stop words and non-alphabetic tokens.

    Parameters:
        texts (list of str): List of text entries to process.

    Returns:
        Counter: A Counter object with lemmatized word frequencies.
    """
    word_freq = Counter()
    for doc in nlp.pipe(texts, disable=['ner', 'parser']):
        word_freq.update([token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop])
    return word_freq

def word_frequency_with_lemmatization(input_file):
    """
    Count word frequencies in a CSV file and save results.

    Reads a CSV file, extracts text data from a specific column, lemmatizes 
    and counts word frequencies, and saves the results to a new CSV file.

    Parameters:
        input_file (str): Path to the input CSV file.

    Raises:
        IOError: If there is an issue reading from `input_file` or writing to the output file.
        IndexError: If the specified text column does not exist in the input file.
    """
    df = pd.read_csv(input_file)

    text_column = df.iloc[:, 4].dropna().astype(str)  # df.iloc[:, x] where x refers to the column index
    
    # Perform lemmatization and word frequency counting
    word_freq = lemmatize_and_count(text_column)
    
    # Convert the frequency counter to a DataFrame
    word_freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
    word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)
    
    # Create output file name based on the input file name
    output_file = 'word_freq_' + os.path.basename(os.path.normpath(input_file))
    
    # Save the word frequency data to a CSV file
    word_freq_df.to_csv(output_file, index=False)
    print(f'Word frequency saved to {output_file}')


if __name__ == "__main__":
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/summaries'
    for filename in os.listdir(directory):
        print(filename)
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            word_frequency_with_lemmatization(f)
