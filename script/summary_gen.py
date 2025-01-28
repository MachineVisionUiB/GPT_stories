import pandas as pd
import openai
import os
from dotenv import load_dotenv
from collections import Counter
import re
from datetime import date


def load_api_key():
    """
    Loads the OpenAI API key from environment variables.
    """
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key not found. Please check your .env file or environment variables.")
    
    openai.api_key = api_key





def generate_summary(countries):
    """
    Analyzes stories from CSV files in a directory using OpenAI's GPT model.

    Parameters
    ----------
    directory : str
        Path to the directory containing CSV files with stories.

    Returns
    -------
    dict
        A dictionary of DataFrames, where keys are filenames and values are DataFrames
        with the original stories and identified names/places.
    """
    
    filepath = f"../data/{countries}/{countries}_stories.csv"
    print(f'Generating plot summary from {filepath}...\n')
    
    results = []
    df = pd.read_csv(filepath)

    for index, row in df.iterrows():
        story = row['Story']
        print(f"•Processing story {index + 1} of {len(df)}...")

        prompt = f"Write a 50 word plot summary of this story:\n\n{story}"

        # Get main character name
        messages = messages = [{"role": "system", "content": ""}]
        messages.append({"role": "user", "content": prompt})
        main_char_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
        )
        plot_sum = main_char_response.choices[0].message.content.strip()
        results.append(plot_sum)
    df.insert(5, 'Summaries', results)
    df["Prompt"] = "Write a 100 word plot summary of this story: [story]"
    df["Date"] = date.today().strftime("%d-%m-%Y")
    output_filepath = f'../data/{countries}/{countries}_summaries_100.csv'
    df.to_csv(output_filepath, index=False)
    return df



def main(countries, startfrom):
    # Load the API key
    load_api_key()

    if 'all' in countries and len(countries) == 1:
        for dir in sorted(os.listdir("../data")):
            if startfrom != "" and startfrom != dir:
                continue
            else:
                startfrom = ""
                generate_summary(dir)
    
    else:
        for dir in sorted(os.listdir("../data")):
            if dir in countries:
                generate_summary(dir)



if __name__ == "__main__":
    main()
