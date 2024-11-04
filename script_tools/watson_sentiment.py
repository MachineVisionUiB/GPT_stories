import json
import pandas as pd
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.api_exception import ApiException
import time
import os

# Replace these variables with your own values
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
directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/summaries'
csv_file_paths = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        csv_file_paths.append(f)

output_data = []  # List to store output data

# Read each specified CSV file and perform analysis
for csv_file in csv_file_paths:
    print(f"Analyzing emotions in {csv_file}...")
    df = pd.read_csv(csv_file)  # Read each CSV file
    for index, row in df.iterrows():
        text_to_analyze = row[4]  # choose the column in the []. [1] is the second column
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

            # Create a DataFrame from the output data and save to CSV
            output_df = pd.DataFrame(output_data)

             # Calculate averages for each emotion and append as a new row
            if not output_df.empty:
                averages = output_df[['sadness', 'joy', 'fear', 'disgust', 'anger']].mean().round(2)
                avg_row = pd.DataFrame([['Averages'] + averages.tolist()], columns=output_df.columns)
                output_df = pd.concat([output_df, avg_row], ignore_index=True)

            filename = os.path.basename(os.path.normpath(csv_file))
            output_df.to_csv('emotion_analysis_' + filename, index=False)

print("Emotion analysis completed and saved to emotion_analysis_output.csv")
