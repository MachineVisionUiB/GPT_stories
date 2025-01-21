import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import os

def sentiment_analysis(directory):
    """
    Perform sentiment analysis on all CSV files in a directory and return a concatenated DataFrame.
    """
    dfs = []
    model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Create a sentiment-analysis pipeline
    sentiment_analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, device=0)

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f) and f.endswith('.csv'):
            df = pd.read_csv(f)

            # Extract text data from the specified column (adjust the index if needed)
            texts = df.iloc[:, 1].tolist()

            # Apply sentiment analysis to the list of texts
            results = sentiment_analyzer(texts)

            # Append sentiment labels and confidence scores to the DataFrame
            df['sentiment'] = [result['label'] for result in results]
            df['confidence'] = [round(result['score'], 2) for result in results]

            # Keep track of the filename
            df['filename'] = filename
            dfs.append(df)

    # Concatenate all DataFrames
    return pd.concat(dfs, ignore_index=True)

def count_high_scoring_sentiments(input_df, threshold=0.85):
    """
    Count high-scoring sentiment entries in a single DataFrame and return the results as a DataFrame.
    """
    # Filter rows based on the confidence score threshold
    high_confidence = input_df[input_df['confidence'] >= threshold]

    # Count sentiments grouped by filename and sentiment
    results = high_confidence.groupby(['filename', 'sentiment']).size().reset_index(name='count')
    
    return results

def main(countries, startfrom):

    if 'all' in countries and len(countries) == 1:
        for dir in sorted(os.listdir("../data")):
            if startfrom != "" and startfrom != dir:
                continue
            else:
                startfrom = ""
                analyzed_sent = analyse_and_save(dir)
    
    else:
        for dir in sorted(os.listdir("../data")):
            if dir in countries:
                analyse_and_save(dir)


    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/full_stories2'
    input_df = sentiment_analysis(directory)
    print("Sentiment Analysis Output:")
    print(input_df.head())  # Preview the combined DataFrame

    output_df = count_high_scoring_sentiments(input_df)
    print("\nHigh-Scoring Sentiments Count:")
    print(output_df.head())  # Preview the results
    output_df.to_csv('high_scoring_sentiments.csv', index=False)  # Save the results to a CSV file
    return output_df

if __name__ == "__main__":
    main()
