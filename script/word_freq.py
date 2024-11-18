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

def word_frequency_with_lemmatization(input_file):
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
    df = pd.read_csv(input_file)

    # Extract the target text column for processing
    text_column = df.iloc[:, 4].dropna().astype(str)  # Adjust column index if necessary

    # Perform lemmatization and count word frequencies
    word_freq = lemmatize_and_count(text_column)

    # Convert the frequency data to a DataFrame and sort by frequency
    word_freq_df = pd.DataFrame(word_freq.items(), columns=['Word', 'Frequency'])
    word_freq_df = word_freq_df.sort_values(by='Frequency', ascending=False)

    # Create output file name based on input file name
    output_file = 'word_freq_' + os.path.basename(os.path.normpath(input_file))

    # Save the word frequency data to a CSV file
    word_freq_df.to_csv(output_file, index=False)
    print(f'Word frequency saved to {output_file}')



def main():
    # Load SpaCy's English language model
    nlp = spacy.load('en_core_web_sm')
    # Specify directory containing CSV files
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/summaries'
    
    # Process each file in the directory
    for filename in os.listdir(directory):
        print(filename)
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            word_frequency_with_lemmatization(f, nlp)


if __name__ == "__main__":
    main()
