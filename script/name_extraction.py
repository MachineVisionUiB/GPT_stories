import pandas as pd
import openai
import os
from dotenv import load_dotenv
from collections import Counter
import re


def load_api_key():
    """
    Loads the OpenAI API key from environment variables.
    """
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key not found. Please check your .env file or environment variables.")
    
    openai.api_key = api_key


def initiate_chat():
    
    messages = [{"role": "system", "content": ""}]
    messages.append({"role": "user", "content": """Identify the name of the main character and only the name of the main character in this story:\n\n**Chapter 1: The Call of the Grove**

In a small village nestled between the misty hills of southern China, legends whispered through the air like a gentle breeze. The villagers of Xianglin spoke of the Wu Yi Bamboo Grove, a place where the wind carried the secrets of the ancients and where the spirits of nature danced under the moonlight. For centuries, the grove had remained untouched, a sanctuary for those seeking solace from the tumult of life.

Li Mei, a spirited young woman of twenty, had always felt a magnetic pull towards the grove. With her raven-black hair cascading in soft waves and her almond-shaped eyes shimmering with curiosity, she often wandered to the edge of the forest, listening to the rustle of the bamboo. The villagers warned her of the grove's powers, tales of lost souls and enchanting encounters, but Li Mei's heart was a canvas painted with dreams, and fear was merely a distant shadow.

One fateful evening, as the sun dipped below the horizon, casting a golden hue over the landscape, Li Mei made her decision. She would venture into the grove, driven by an insatiable hunger for understanding, for connection with the world around her. With a woven basket on her arm, filled with offerings of rice cakes and incense, she stepped into the emerald embrace of the bamboo.

The path was narrow, winding like a serpent, flanked by towering stalks that swayed gently with the evening breeze. On the way she saw visions of her friend, Sung Lee. As she walked deeper into the grove, the air thickened with an otherworldly presence. Shadows danced, and the soft sound of whispers brushed against her ears. ""Welcome,"" they seemed to say, ""we’ve been waiting for you."""})
    messages.append({"role": "system", "content": "Li Mei"})
    
    return messages


def analyze_stories(directory):
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
    dfs = {}

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Ensure 'Story' column exists
        if 'Story' not in df.columns:
            print(f"Skipping {filename}: 'Story' column not found.")
            continue

        # Initialize lists for storing GPT results
        results_names = []

        for index, row in df.iterrows():
            story = row['Story']
            print(f"Analyzing story {index + 1} of {len(df)} in {filename}...")

            # Prepare prompts
            main_char_prompt = f"Identify the name of the main character and only the name of the main character in this story:\n\n{story}"
            place_name_prompt = f"Identify the name of the places (only real place names) and only the name of the places in this story:\n\n{story}"

            # Get main character name
            messages = initiate_chat()
            messages.append({"role": "user", "content": main_char_prompt})
            main_char_response = openai.chat.completions.create(
                model="gpt-4-0613",
                messages=messages,
                temperature=0.8,
                max_tokens=50,
            )
            main_char = main_char_response.choices[0].message.content.strip()
            results_names.append(main_char)

            

        # Add results to DataFrame
        df['Name'] = results_names

        # Store the updated DataFrame
        dfs[filename] = df

    return dfs


def count_names(dataframes):
    """
    Counts occurrences of names in the 'Name' column across multiple DataFrames.

    Parameters
    ----------
    dataframes : dict
        A dictionary of DataFrames where the 'Name' column contains names to count.

    Returns
    -------
    dict
        A dictionary where keys are filenames and values are DataFrames with name counts.
    """
    result_counts = {}

    for filename, df in dataframes.items():
        if 'Name' not in df.columns:
            print(f"Skipping {filename}: 'Name' column not found.")
            continue

        # Extract and count names
        names = []
        for name_list in df['Name']:
            split_names = re.split(r',|\d+\.\s*|[^a-zA-Z\s]+', name_list)
            names.extend([name.strip() for name in split_names if name.strip()])

        name_counts = Counter(names)

        # Create a new DataFrame for counts
        counts_df = pd.DataFrame(name_counts.items(), columns=['Name', 'Count']).sort_values(by='Count', ascending=False)
        result_counts[filename] = counts_df

    return result_counts


def main():
    # Load the API key
    load_api_key()

    # Directory containing CSV files
    input_directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/full_stories2'

    # Analyze stories and get DataFrames
    analyzed_dataframes = analyze_stories(input_directory)
    print(analyzed_dataframes)

    # Count names in the analyzed DataFrames
    name_counts = count_names(analyzed_dataframes)

    # Print or process the results
    for filename, counts_df in name_counts.items():
        counts_df.to_csv(f'output_{filename}', index=False)
        print(f"Results for {filename}:")
        print(counts_df.head())  # Display top counts for each file


if __name__ == "__main__":
    main()
