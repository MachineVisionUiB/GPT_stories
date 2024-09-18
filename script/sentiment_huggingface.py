import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline

# Load the CSV file
input_filename = input("Enter the input filename: ")+'.csv'

df = pd.read_csv('/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/countries_samples/'+input_filename)

texts = df.iloc[:, 1].tolist()

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

output_filename = input("Enter the output filename: ")
# Save the updated DataFrame to a new CSV file
df.to_csv(output_filename+'_sentiment_hf.csv', index=False)