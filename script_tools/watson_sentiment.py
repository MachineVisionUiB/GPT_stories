import json
import pandas as pd
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.api_exception import ApiException
import time
import os

# Replace these variables with your own values
# should I somehow refer to the documentation for the API key and URL?
api_key = 'FlCsPXUVqv472VYMKv5H5Q935eX9p-_qsM6GOHld6pkE'
url = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/51702159-6356-4e72-8f69-f2de11aa007c'

# Set up the authenticator and NLU service
authenticator = IAMAuthenticator(api_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(url)

# Function to analyze text and return emotion scores
def analyze_emotions(text):
    try:
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(emotion=EmotionOptions())
        ).get_result()
        return response['emotion']['document']['emotion']
    except ApiException as e:
        if e.code == 429:  # Too Many Requests
            print("Rate limit exceeded. Retrying after a delay...")
            time.sleep(10)  # Wait before retrying (adjust as needed)
            return analyze_emotions(text)  # Retry the analysis
        else:
            print(f"Error: {e}")
            return None

# Specify the file paths manually
# Directory containing the CSV files
directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/full_stories'

# Iterate directly through the directory
for filename in os.listdir(directory):
    csv_file = os.path.join(directory, filename)
    if os.path.isfile(csv_file):
        print(f"Analyzing emotions in {csv_file}...")
        df = pd.read_csv(csv_file)  # Read each CSV file
        output_data = []  # Reset output data for each file

        for index, row in df.iterrows():
            text_to_analyze = row[1]  # Choose the column index, here the second column
            emotions = analyze_emotions(text_to_analyze)  # Analyze emotions
            if emotions:  # Proceed only if analysis was successful
                output_data.append({
                    'stories': text_to_analyze,
                    'sadness': emotions['sadness'],
                    'joy': emotions['joy'],
                    'fear': emotions['fear'],
                    'disgust': emotions['disgust'],
                    'anger': emotions['anger']
                })
    # Create a DataFrame from the output data and save to a new CSV
    output_df = pd.DataFrame(output_data)

    # Calculate averages for each emotion and append as a new row
    if not output_df.empty:
        averages = output_df[['sadness', 'joy', 'fear', 'disgust', 'anger']].mean().round(2)
        avg_row = pd.DataFrame([['Averages'] + averages.tolist()], columns=output_df.columns)
        output_df = pd.concat([output_df, avg_row], ignore_index=True)

    # Save the output with a unique filename based on the input filename
    output_filename = f"emotion_analysis_{os.path.basename(csv_file)}"
    output_path = os.path.join(directory, output_filename)
    output_df.to_csv(output_path, index=False)
    print(f"Emotion analysis saved to {output_filename}")

print("Emotion analysis completed.")
