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

    Raises
    ------
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
    to extract the name of the main character, and saves the results (including the 
    original story and the identified main character) to a new CSV file.

    Parameters
    ----------
    csv_file_path : str
        The path to the input CSV file containing the stories to be analyzed.

    Returns
    -------
    None
        The function saves the results to a new CSV file but doesn't return anything.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Initialize a list to store analysis results
    results = []

    # Iterate through each story in the DataFrame
    for index, row in df.iterrows():
        story = row['Story']  # Get the story from the current row
        print(f"Analyzing story {index + 1} of {len(df)}...")

        # Prepare the prompt for the GPT model to identify the main character
        messages = [
            {"role": "user", "content": f"Identify the name of the main character and only the name of the main character in this story:\n\n{story}"}
        ]

        # Send the story to the GPT model for analysis
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            n=1,
            max_tokens=300
        )

        # Extract the main character's name from the response
        main_char = response.choices[0].message.content
        
        # Append the original story and main character to the results list
        results.append((story, main_char))
    
    # Add the identified main characters to the DataFrame as a new column
    df['main_char'] = [result[1] for result in results]

    # Prompt the user for an output file name and save the updated DataFrame
    output_file = input("Enter the output file name: ") + "_" + "mainchar" + '.csv'
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

    # Notify the user that the analysis is complete
    print(f"Analysis complete. Results saved to {output_file}")


if __name__ == "__main__":
    """
    Entry point for the script.

    This section of the code calls the `analyze_stories` function with a specified
    CSV file path containing the stories to be analyzed.
    """
    # Call the analyze_stories function with the input CSV file path
    analyze_stories("/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/countries_samples_50words/norwegian_stories.csv")
