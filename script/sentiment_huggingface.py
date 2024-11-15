import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import os

# Set the directory containing the CSV files
directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/summaries'

for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        df = pd.read_csv(f)

        # Extract text data from the specified column (adjust the index if needed)
        texts = df.iloc[:, 4].tolist()  # df.iloc[:, x] where x is the column index

        # Load the pre-trained model and tokenizer for emotion analysis
        model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)

        # Create a sentiment-analysis pipeline
        sentiment_analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, device=0)

        # Apply sentiment analysis to the list of texts
        results = sentiment_analyzer(texts)

        # Append sentiment labels and confidence scores to the DataFrame
        df['sentiment'] = [result['label'] for result in results]
        df['confidence'] = [round(result['score'], 2) for result in results]

        # Generate the output filename with a prefix and save the updated DataFrame to a new CSV file
        output_filename = 'hf_' + filename
        df.to_csv(output_filename, index=False)
