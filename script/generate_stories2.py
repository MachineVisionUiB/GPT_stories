import os
import openai
import pandas as pd
from dotenv import load_dotenv
import csv
from datetime import date
import time

def load_api_key():
    """
    Loads the OpenAI API key from environment variables.

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

def get_prompt(country_name, stories):
    """
    Generates a detailed storytelling prompt based on the country name.

    Parameters
    ----------
    country_name : str
        The name of the country for which stories should be generated.
    stories : list
        A list of previously generated stories to ensure uniqueness.

    Returns
    -------
    str
        A formatted prompt string.
    """
    prompt = f'''"You are a master storyteller with deep knowledge of global cultures, geographies, and archetypal themes. Your task is to create 50 unique stories for this country: {country_name}. Each story must adhere to the following guidelines:

1. Length: Approximately 1000 words.
2. Language: Written in English, inspired by the country's native language and culture.
3. Diversity in Form and Content: Each story should be unique in style, genre, and theme.
4. Cultural Authenticity: Stories should reflect the country's culture, history, and geography.
5. Unique Settings: No two stories should have the same setting.
6. Character Diversity: Protagonists should vary in age, gender, profession, and background.
7. Language and Style: Incorporate local idioms, proverbs, and storytelling traditions.
8. Avoid Stereotypes: Ensure depth and nuance while avoiding clichés.

Begin by researching {country_name}'s cultural and geographical diversity. Then, craft 50 stories that collectively paint a rich, multifaceted portrait of the country. Take into consideration the stories that have already been written and ensure that each new story adds a fresh perspective or dimension to the collection: {stories}'''
    
    return prompt

def generate_stories(number_of_stories_per_topic: int, demonym: str, country_code: str, country_name: str):
    """
    Generates stories using the OpenAI API.

    Parameters
    ----------
    number_of_stories_per_topic : int
        Number of stories to generate per country.
    demonym : str
        The demonym of the country (e.g., 'Norwegian' for Norway).
    country_code : str
        The ISO 3166-1 code of the country.
    country_name : str
        The full name of the country.

    Returns
    -------
    list
        A list of tuples containing story metadata.
    """
    word_count = 1500
    previous_stories = []
    stories = []
    gpt_model = "gpt-4o-mini"
    temperature = 0.8

    for story_iteration in range(number_of_stories_per_topic):
        print(f"\nGenerating story {story_iteration+1} of {number_of_stories_per_topic} for {country_name}...\n")
        prompt = get_prompt(country_name, previous_stories)
        messages = [{"role": "system", "content": ""}, {"role": "user", "content": prompt}]
        
        response = openai.chat.completions.create(
            model=gpt_model,
            messages=messages,
            temperature=temperature,
        )
        
        story = response.choices[0].message.content
        previous_stories.append(story)
        print(f'{story}\n---------------------------------\n\n')

        story_id = f"{country_code}_{story_iteration+1}"
        timestamp = date.today().strftime("%d-%m-%Y")
        
        stories.append((story_id, country_code, country_name, demonym, story, prompt, timestamp, gpt_model, temperature))
    
    return stories

def create_dataset(stories, country_code):
    """
    Saves the generated stories to a CSV file.

    Parameters
    ----------
    stories : list of tuples
        List containing story data.
    country_code : str
        ISO 3166-1 country code.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the generated stories.
    """
    df = pd.DataFrame(stories, columns=['Story_ID', 'ISO-3166-1', 'Country_Name', 'Demonym', 'Story', 'Prompt', 'Date', 'GPT_Model', 'Temperature'])
    
    directory = f"../data2/{country_code}"
    os.makedirs(directory, exist_ok=True)
    filepath = f"{directory}/{country_code}_stories.csv"
    
    df.to_csv(filepath, index=False, quoting=csv.QUOTE_ALL)
    print(f"Dataset saved to {filepath}\n")
    
    return df

def main(num_story_per_topic, demonym, country_code, country_name):
    """
    Main function to load API key, generate stories, and save them to a dataset.

    Parameters
    ----------
    num_story_per_topic : int
        Number of stories per country.
    demonym : str
        The demonym of the country.
    country_code : str
        The ISO 3166-1 country code.
    country_name : str
        The full name of the country.
    
    Returns
    -------
    pandas.DataFrame
        A dataset containing the generated stories.
    """
    load_api_key()
    stories = generate_stories(num_story_per_topic, demonym, country_code, country_name)
    return create_dataset(stories, country_code)

if __name__ == "__main__":
    main()
