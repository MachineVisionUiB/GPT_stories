import pandas as pd
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
from datetime import date
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

    filepath = f"../data/{directory}/{directory}_summaries.csv"
    
    df = pd.read_csv(filepath)

    # Extract text data from the specified columns (adjust the index if needed)
    texts = df.iloc[:, 5].tolist()
    story_ids = df.iloc[:, 0].tolist()

    # Apply sentiment analysis to the list of texts
    results = sentiment_analyzer(texts)


    sentiment_df = pd.DataFrame()
    sentiment_df['story_id'] = story_ids
    sentiment_df['sentiment'] = [result['label'] for result in results]
    sentiment_df['confidence'] = [round(result['score'], 2) for result in results]
    sentiment_df['model'] = model_name
    sentiment_df['date'] = date.today().strftime("%d-%m-%Y") 

    sentiment_df.to_csv(f'../data/{directory}/{directory}_sentiments.csv', index=False)  # Save the DataFrame to a CSV file





def main(countries, startfrom):
    if 'all' in countries and len(countries) == 1:
        for dir in sorted(os.listdir("../data")):
            if startfrom != "" and startfrom != dir:
                continue
            else:
                startfrom = ""
                sentiment_analysis(dir)
                
    
    else:
        for dir in sorted(os.listdir("../data")):
            if dir in countries:
                sentiment_analysis(dir)
                

    

if __name__ == "__main__":
    main()
