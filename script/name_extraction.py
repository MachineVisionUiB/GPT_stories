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

    messages.append({"role": "user", "content": """Identify the name of the main character and only the name of the main character in this story:\n\nA In a quiet village near the Caspian Sea, an old fisherman discovered a shimmering, ancient lantern buried in the sand. When he rubbed it, a gentle spirit emerged, offering wishes. Torn between personal desires and the needs of his struggling community, he chose to share his fortune, transforming their lives forever. If the main character's name is not mentioned, please type 'Unknown'."""})
    messages.append({"role": "system", "content": "Unknown"})

    messages.append({"role": "user", "content": """Identify the name of the main character and only the name of the main character in this story:\n\nA forgotten letter reveals secrets, changing a family's destiny forever. If the main character's name is not mentioned, please type 'Unknown'."""})
    messages.append({"role": "system", "content": "Unknown"})
    
    return messages


def analyze_stories(countries):
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
    print(f'Extracting main character names from {filepath}...\n')
    
    results_names = []
    df = pd.read_csv(filepath)

    for index, row in df.iterrows():
        story = row['Story']
        print(f"•Processing story {index + 1} of {len(df)}...")

        main_char_prompt = f"Identify the name of the main character and only the name of the main character in this story:\n\n{story}"

        # Get main character name
        messages = initiate_chat()
        messages.append({"role": "user", "content": main_char_prompt})
        main_char_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            max_tokens=50,
        )
        main_char = main_char_response.choices[0].message.content.strip()
        results_names.append(main_char)

    # Add results to DataFrame
    df['Name'] = results_names

    return df



def count_names(dict_with_names):
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

    names = []
    
    for name_list in dict_with_names['Name']:
        split_names = re.split(r',|\d+\.\s*|[^a-zA-Z\s]+', name_list)
        names.extend([name.strip() for name in split_names if name.strip()])

    name_counts = Counter(names)

    # Create a new DataFrame for counts
    counts_df = pd.DataFrame(name_counts.items(), columns=['Name', 'Count']).sort_values(by='Count', ascending=False)
    return counts_df


def analyse_and_save(dir):
    analyzed_dataframe = analyze_stories(dir)
    
    # Count names in the analyzed DataFrames
    name_count = count_names(analyzed_dataframe)
    output_filepath = f"../data/{dir}/{dir}_names.csv"

    print(f"\nTop results for {output_filepath}:\n")
    print(f'{name_count.head()}')  # Display top counts for each file

    name_count.to_csv(output_filepath, index=False)
    print(f'\nMain character names saved to {output_filepath}\n\n--------------------\n')



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
                analyse_and_save(dir)
    
    else:
        for dir in sorted(os.listdir("../data")):
            if dir in countries:
                analyse_and_save(dir)



if __name__ == "__main__":
    main()
