import os
import openai
import pandas as pd
from dotenv import load_dotenv
import csv
from datetime import date



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


def generate_stories(number_of_stories_per_topic: int, demonym: str, country_code: str, country_name: str):
    """
    Generates potential stories using the OpenAI API.

    This function takes a takes a demonym, country code and country name from a specific counrty.
    For each country, the specified number of stories are generated 
    and saved as a pdf and a list of tuples is returned.

    Parameters
    ----------
    number_of_stories_per_topic : int
        The number of stories to generate for each topic.
    demonym : str
        The demonym for the country.
    country_code : str
        The ISO-3166-1 alpha-2 code for the country.
    country_name : str
        The name of the country.

    Returns
    -------
    list
        A list of tuples containing the story_id, story, prompt, topic, and time.

    Example
    -------
    >>> generate_stories(["Norwegian", "Japanese"], 2)
    """
    
    word_count = 1500 # Number of words for each story

    # Generate prompts based on country
    if country_code == 'XX':    
        prompt = f"Write a {word_count} word potential story." 
    else:
        prompt = f"Write a {word_count} word potential {demonym} story."  # Generate prompts based on topics
    stories = []

    # Choose GPT model and temperature
    gpt_model = "gpt-4o-mini"
    temperature = 0.8

    # Calling the OpenAI API to generate stories
    for story_iteration in range(number_of_stories_per_topic):
        print(f"\nGenerating story {story_iteration+1} of {number_of_stories_per_topic} for {country_name}...\n")
        messages = [{"role": "system", "content": ""}]  # Initial system message
        messages.append({"role": "user", "content": prompt})
        response = openai.chat.completions.create(
            model=gpt_model,
            messages=messages,
            temperature=temperature,
        )
        # Extract generated story from the response
        story = response.choices[0].message.content
        print(f'{story}\n---------------------------------\n\n')
        # Create a unique identifier for each story
        story_id = f"{country_code}_{story_iteration+1}"

        time = date.today().strftime("%d-%m-%Y")
        stories.append((story_id, country_code, country_name, demonym, story, prompt, time, gpt_model, temperature))
        
    return stories


def create_dataset(stories, country_code):
    """
    Creates a CSV file from the generated stories.

    This function takes the generated stories, which are stored in a list of tuples,
    and writes them to a CSV file using pandas. 

    Parameters
    ----------
    stories : list of tuples
        Each tuple contains (story_id, country_code, country_name, demonym, story, prompt, date, gpt_model, temperature).

    """
    # Create a DataFrame from the stories list
    df = pd.DataFrame(stories, columns=['Story_ID', 'ISO-3361', 'Country_Name', 'Demonym', 'Story', 'Prompt', 'Date', 'GPT_Model', 'Temperature'])

    
    # Create a directory to store the data if it does not exist
    directory = "../data2/"+country_code
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    # Create a unique filename for the dataset based on the country code
    filepath = f"{directory}/{country_code}_stories.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(filepath, index=False, quoting=csv.QUOTE_ALL)

    print(f"Dataset saved to {filepath}\n")


def main(num_story_per_topic, demonym, country_code, country_name):
    # Load the API key when the module is imported
    load_api_key()

    # Generate stories based on countries and save to CSV
    stories = generate_stories(num_story_per_topic, demonym, country_code, country_name)
    create_dataset(stories, country_code)
    



if __name__ == "__main__":
    main()


    
