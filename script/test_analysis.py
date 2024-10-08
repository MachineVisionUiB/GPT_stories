import pandas as pd
import openai
import csv
from dotenv import load_dotenv
import os

def load_api_key():
    """
    Loads the OpenAI API key from environment variables.

    This function uses python-dotenv to load environment variables from a .env file,
    retrieves the OPENAI_API_KEY, and sets it for the OpenAI client. If the API key
    is not found, it raises a ValueError.

    Raises:
    -------
    ValueError
        If the API key is not found in the environment variables.
    """
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key not found. Please check your .env file or environment variables.")
    
    openai.api_key = api_key

# Load the API key when the module is imported
load_api_key()

def analyze_stories(csv_file_path: str):
    """
    Analyzes stories from a CSV file using OpenAI's GPT model.

    This function reads stories from a CSV file, sends each story to the GPT model
    for analysis, and saves the results (including the original story, the analysis,
    and step-by-step reasoning) to a new CSV file.

    Parameters
    ----------
    csv_file_path : str
        The path to the input CSV file containing the stories to be analyzed.

    Returns
    -------
    None
        The function saves the results to a new CSV file but doesn't return anything.
    """
    # Read the csv file
    df = pd.read_csv(csv_file_path)
    # Initialize list to store analysis results
    results = []

    # Iterate through each story in the DataFrame
    for index, row in df.iterrows():
        story = row['Story']
        
        # Prepare the initial message for the GPT model
        messages = [
            {"role": "user", "content": f"Identify the main themes and character roles in this story.:\n\n{story}"}
        ]

        # Send the story to the GPT model for analysis
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            n=1,
            max_tokens=300
        )

        # Extract the analysis and reasoning from the model's response
        analysis_and_reasoning = response.choices[0].message.content
        
        # Append results to list
        results.append((story, analysis_and_reasoning))
    
    # Add new columns to the DataFrame
    df['Analysis and Reasoning'] = [result[1] for result in results]

    # Save the updated DataFrame to a new CSV file
    output_file = "analyzed_stories_single_prompt_test.csv"
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

    print(f"Analysis complete. Results saved to {output_file}")

if __name__ == "__main__":
    # Call the analyze_stories function with the input CSV file
    analyze_stories("test_stories.csv")