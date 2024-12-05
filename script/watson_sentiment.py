import json
import pandas as pd
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.api_exception import ApiException
import time
import os

# Replace these variables with your own IBM Watson NLU API credentials
api_key = 'FlCsPXUVqv472VYMKv5H5Q935eX9p-_qsM6GOHld6pkE'
url = 'https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/51702159-6356-4e72-8f69-f2de11aa007c'

# Set up the authenticator and NLU service
authenticator = IAMAuthenticator(api_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(url)

def analyze_emotions(text):
    """
    Analyze the emotions present in the provided text using IBM Watson's NLU.

    This function uses the IBM Watson Natural Language Understanding API to
    perform an emotion analysis on the given text, returning a dictionary
    with scores for each emotion (sadness, joy, fear, disgust, anger).
    It handles rate limiting by retrying with a delay if necessary.

    Args:
        text (str): The text to analyze for emotions.

    Returns:
        dict: A dictionary containing emotion scores if successful, or None if
              there was an error.
    """
    try:
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(emotion=EmotionOptions())
        ).get_result()
        return response['emotion']['document']['emotion']
    except ApiException as e:
        if e.code == 429:  # Too Many Requests
            print("Rate limit exceeded. Retrying after a delay...")
            time.sleep(10)  # Wait before retrying
            return analyze_emotions(text)  # Retry the analysis
        else:
            print(f"Error: {e}")
            return None
        


def data_processing(input):
    # Directory and CSV file paths
    directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/full_stories'
    csv_file_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]

    # Process each CSV file and perform emotion analysis
    for csv_file in csv_file_paths:
        print(f"Analyzing emotions in {csv_file}...")
        df = pd.read_csv(csv_file)  # Load the current CSV file
        output_data = []  # Reset output data for each file

        for index, row in df.iterrows():
            text_to_analyze = row[1]  # Adjust column index as needed
            emotions = analyze_emotions(text_to_analyze)  # Perform emotion analysis
            if emotions:  # Only proceed if analysis was successful
                output_data.append({
                    'stories': text_to_analyze,
                    'sadness': emotions['sadness'],
                    'joy': emotions['joy'],
                    'fear': emotions['fear'],
                    'disgust': emotions['disgust'],
                    'anger': emotions['anger']
                })

        # Create a DataFrame from the collected emotion data and save it
        output_df = pd.DataFrame(output_data)

        # Calculate emotion averages and append them as a summary row
        if not output_df.empty:
            averages = output_df[['sadness', 'joy', 'fear', 'disgust', 'anger']].mean().round(2)
            avg_row = pd.DataFrame([['Averages'] + averages.tolist()], columns=output_df.columns)
            output_df = pd.concat([output_df, avg_row], ignore_index=True)

        # Save the results to a new CSV file with a unique name
        output_filename = f"emotion_analysis_{os.path.basename(csv_file)}"
        output_path = os.path.join(directory, output_filename)
        output_df.to_csv(output_path, index=False)
        print(f"Emotion analysis saved to {output_filename}")

print("Emotion analysis completed.")


def main(api_key, url):
    pass

if __name__ == "main":
    main()