import pandas as pd
import spacy
from collections import Counter
import os



def lemmatize_and_count(texts, nlp):
    """
    Perform lemmatization on a list of texts and count word frequencies.

    This function uses SpaCy to lemmatize the words in the provided texts and
    counts the frequency of each lemma that is an alphabetic word and not a stopword.

    Args:
        texts (iterable of str): List or series of texts to process.

    Returns:
        Counter: A Counter object with word frequencies.
    """
    word_freq = Counter()
    for doc in nlp.pipe(texts, disable=['ner', 'parser']):
        word_freq.update([token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop])
    return word_freq

def word_frequency_with_lemmatization(dir, nlp):
    """
    Calculate word frequencies with lemmatization for text in a specified column of a CSV file.

    Reads a CSV file, extracts a column of text, lemmatizes the words, and calculates
    the frequency of each unique lemma. The results are saved to a new CSV file with
    frequencies in descending order.

    Args:
        input_file (str): The path to the input CSV file.

    Returns:
        None
    """

    list_of_names = get_names(dir)

    filepath = f'../data/{dir}/{dir}_stories.csv'
    print(f'\nCalculating word frequencies for {filepath}...\n')

    df = pd.read_csv(filepath)

    # Extract the target text column for processing
    text_column = df.iloc[:, 4].dropna().astype(str)  # Adjust column index if necessary

    # Perform lemmatization and count word frequencies
    word_freq = lemmatize_and_count(text_column, nlp)

    # Convert the frequency data to a DataFrame and sort by frequency
    word_freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
    word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)

    # Filter out names
    word_freq_df = word_freq_df[~word_freq_df['Word'].isin(list_of_names)]

    print(f"Top results for {filepath}:\n")
    print(f'{word_freq_df.head()}')  # Display top counts for each file

    # Create output file name based on input file name
    output_file = f'../data/{dir}/{dir}_word_freq.csv'

    # Save the word frequency data to a CSV file
    word_freq_df.to_csv(output_file, index=False)
    print(f'\nWord frequency saved to {output_file}\n\n--------------------\n')

def get_names(dir):
    """
    Get a list of names from a text file and lower.
    """
    with open(f'../data/{dir}/{dir}_names.csv', 'r') as f:
        df = pd.read_csv(f)
        names = df['Name'].str.lower().tolist()
        
    return names


def main(countries, startfrom):
    # Load SpaCy's English language model
    nlp = spacy.load('en_core_web_sm')
    
    if 'all' in countries and len(countries) == 1:
        for dir in sorted(os.listdir(f'../data/')):
            if dir == '.DS_Store':
                continue
            if startfrom != "" and startfrom != dir:
                continue
            else:
                startfrom = ""
                word_frequency_with_lemmatization(dir, nlp)
    else:
        for dir in sorted(os.listdir(f'../data/')):
            if dir in countries:
                word_frequency_with_lemmatization(dir, nlp)
    


if __name__ == "__main__":
    main()
