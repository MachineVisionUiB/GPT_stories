import pandas as pd
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
import os

def sentiment_analysis(directory):
    """
    Perform sentiment analysis on all CSV files in a directory and return a concatenated DataFrame.
    """
    # dfs = []
    model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

    # Create a sentiment-analysis pipeline
    sentiment_analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, device=0)

    filepath = f"../data/{directory}/{directory}_stories.csv"
    
    df = pd.read_csv(filepath)

    # Extract text data from the specified column (adjust the index if needed)
    texts = df.iloc[:, 5].tolist()

    # Apply sentiment analysis to the list of texts
    results = sentiment_analyzer(texts)

    # Append sentiment labels and confidence scores to the DataFrame
    df['sentiment'] = [result['label'] for result in results]
    df['confidence'] = [round(result['score'], 2) for result in results]

    # Keep track of the filename
    df['filename'] = directory
    

    # Concatenate all DataFrames
    return df

def count_high_scoring_sentiments(input_df, threshold):
    """
    Count high-scoring sentiment entries in a single DataFrame and return the results as a DataFrame.
    """
    # Filter rows based on the confidence score threshold
    high_confidence = input_df[input_df['confidence'] >= threshold]

    # Count sentiments grouped by filename and sentiment
    results = high_confidence.groupby(['filename', 'sentiment']).size().reset_index(name='count')
    
    return results

def main(countries, startfrom):
    dfs = []
    if 'all' in countries and len(countries) == 1:
        for dir in sorted(os.listdir("../data")):
            if startfrom != "" and startfrom != dir:
                continue
            else:
                startfrom = ""
                analyzed_sent = sentiment_analysis(dir)
                dfs.append(analyzed_sent)
    
    else:
        for dir in sorted(os.listdir("../data")):
            if dir in countries:
                analyzed_sent = sentiment_analysis(dir)
                dfs.append(analyzed_sent)
    combined_df = pd.concat(dfs, ignore_index=True)
    print("Sentiment Analysis Output:")
    print(combined_df.head())  # Preview the combined DataFrame
    combined_df.to_csv('all_sentiment_analysis.csv', index=False)  # Save the combined DataFrame to a CSV file

    
    threshold = 0.85  # Set the confidence score threshold
    ranked_df = count_high_scoring_sentiments(combined_df, threshold)
    print("\nHigh-Scoring Sentiments Count:")
    print(ranked_df.head())  # Preview the results
    ranked_df.to_csv(f'all_high_scoring_sentiments_{threshold}.csv', index=False)  # Save the results to a CSV file
    

if __name__ == "__main__":
    main()
