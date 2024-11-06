import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import os

directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/summaries'

for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        df = pd.read_csv(f)

   

        texts = df.iloc[:, 4].tolist() # Adjust if the column index is different. df.iloc[:, x] where x is the column index

        #model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
        model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Create a sentiment-analysis pipeline
        sentiment_analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, device=0)

        # Apply the sentiment analysis
        results = sentiment_analyzer(texts)

        df['sentiment'] = [result['label'] for result in results]
        df['confidence'] = [round(result['score'], 2) for result in results]

        output_filename = 'hf_' + filename

        # Save the updated DataFrame to a new CSV file
        df.to_csv(filename, index=False)