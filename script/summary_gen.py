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





def generate_summary(dir):
    """
    Create summaries of stories from CSV files in a directory using OpenAI's GPT model.

    Parameters
    ----------
    directory : str
        Name of directory containing CSV files with stories.

    Returns
    -------
    dict
        A dictionary of DataFrames, where keys are filenames and values are DataFrames
        with the original stories and identified names/places.
    """
    
    filepath = f"../data/{dir}/{dir}_stories.csv"
    print(f'Generating plot summary from {filepath}...\n')
    
    results = []
    df = pd.read_csv(filepath)

    for index, row in df.iterrows():
        story = row['Story']
        print(f"•Processing story {index + 1} of {len(df)}...")

        prompt = f"Write a 50 word plot summary of this story:\n\n{story}"
        model = "gpt-4o-mini"
        # Get main character name
        messages = messages = [{"role": "system", "content": ""}]
        messages.append({"role": "user", "content": prompt})
        main_char_response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
        )
        plot_sum = main_char_response.choices[0].message.content.strip()
        print('-------------------\n' + plot_sum + '\n-------------------\n\n')
        results.append(plot_sum)

    summary_df = pd.DataFrame()
    story_ids = df.iloc[:, 0].tolist()
    summary_df['Story_ID'] = story_ids
    summary_df['Summaries'] = results
    summary_df['Prompt'] = "Write a 50 word plot summary of this story: [STORY]"
    summary_df['Model'] = model
    summary_df['Date'] = date.today().strftime("%d-%m-%Y") 

    output_filepath = f'../data/{dir}/{dir}_summaries.csv'
    summary_df.to_csv(output_filepath, index=False)
    return df



def main(countries, startfrom):
    # Load the API key
    load_api_key()

    if 'all' in countries and len(countries) == 1:
        for dir in sorted(os.listdir("../data")):
            if dir == '.DS_Store':
                continue
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
