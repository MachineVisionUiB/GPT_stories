import pandas as pd
from textblob import TextBlob
import os



def get_sentiment(text: str):
    """
    Analyzes the sentiment of the given text using TextBlob.

    This function takes a string as input and calculates its polarity and 
    subjectivity using TextBlob's sentiment analysis capabilities.

    Parameters
    ----------
    text : str
        The input text for which the sentiment analysis will be performed.

    Returns
    -------
    tuple
        A tuple containing two float values:
        - polarity (float): The sentiment polarity of the text, ranging from -1 to 1.
        - subjectivity (float): The subjectivity of the text, ranging from 0 to 1.
    """
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    return polarity, subjectivity






def main(countries, startfrom):
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/summaries'

    for filename in os.listdir(directory):
        print(filename)
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            df = pd.read_csv(f)


            # Apply sentiment analysis 
            df[['Polarity', 'Subjectivity']] = df.iloc[:, 4].apply(lambda x: pd.Series(get_sentiment(str(x)))) # Adjust if the column index is different. df.iloc[:, x] where x is the column index


            # Calculate the averages of the Polarity and Subjectivity columns
            average_polarity = round(df['Polarity'].mean(), 2)
            average_subjectivity = round(df['Subjectivity'].mean(), 2)


            # Create a new DataFrame to hold the averages, using 'Average' as a label in the first column
            average_row = pd.DataFrame({'Column1': ['Average'], 'Polarity': [average_polarity], 'Subjectivity': [average_subjectivity]})


            # Append the average row to the original DataFrame
            df_with_avg = pd.concat([df, average_row], ignore_index=True)


            # Prompt the user for the output file name and save the modified DataFrame to a CSV file
            output_filename = 'tb_' + filename
            df_with_avg.to_csv(output_filename, index=False)


if __name__ == "__main__":
    main()