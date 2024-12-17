import os
import openai
import pandas as pd
from dotenv import load_dotenv
import csv
from datetime import date
import time


# time program execution
start_time = time.time()

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
    Generates plot summaries based on a list of topics using the OpenAI API.

    This function takes a list of topics and generates a prompt for each topic.
    For each topic, the specified number of stories are generated 
    and stored in a list.

    Parameters
    ----------
    topics : list[str]
        A list of topics, such as cultures or countries, used to generate story prompts.
    number_of_stories_per_topic : int
        The number of stories to generate for each topic.

    Returns
    -------
    list
        A list of tuples, each containing (story_id, story, prompt, topic).

    Example
    -------
    >>> generate_stories(["Norwegian", "Japanese"], 2)
    """
    
    # word_count = input("Enter the word count: ")  # User input for word count
    word_count = 50
    prompt = f"Write a {word_count} word potential {demonym} story."  # Generate prompts based on topics
    stories = []

    # Choose GPT model and temperature
    gpt_model = "gpt-4o-mini"
    temperature = 0.8

    

    for story_iteration in range(number_of_stories_per_topic):
        messages = [{"role": "system", "content": ""}]  # Initial system message
        messages.append({"role": "user", "content": prompt})
        response = openai.chat.completions.create(
            model=gpt_model,
            messages=messages,
            temperature=temperature,
        )
        # Extract generated story from the response
        story = response.choices[0].message.content
        # Create a unique identifier for each story
        story_id = f"{country_code}_{story_iteration+1}"

        time = date.today().strftime("%d-%m-%Y")
        stories.append((story_id, country_code, country_name, demonym, story, prompt, time, gpt_model, temperature))
        
        # Print the generated story
        # print(f"\nVersion {story_iteration+1}: {story}")

    return stories


def create_dataset(stories, country_code):
    """
    Creates a CSV file from the generated stories.

    This function takes the generated stories, which are stored in a list of tuples,
    and writes them to a CSV file using pandas. 

    Parameters
    ----------
    stories : list of tuples
        Each tuple contains (story_id, story, prompt, topic).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the stories, prompts, and topics.
    """
    # Create a DataFrame from the stories list
    df = pd.DataFrame(stories, columns=['Story_ID', 'ISO-3361', 'Country_Name', 'Demonym', 'Story', 'Prompt', 'Date', 'GPT_Model', 'Temperature'])

    # Generate a unique filename from user input

    directory = "../test_data/"+country_code
    if not os.path.exists(directory):
        os.mkdir(directory)
    filepath = f"{directory}/{country_code}_stories.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(filepath, index=False, quoting=csv.QUOTE_ALL)

    print(f"\nDataset saved to {filepath}\n")

    return df






def prompt_counter_print(prompts, prompt_number):
    """
    Prints the current prompt number and its content.

    This function displays which prompt is currently being processed.

    Parameters
    ----------
    prompts : list
        A list of generated prompts.
    prompt_number : int
        The index of the current prompt being processed.
    """
    num_of_prompts = len(prompts)
    print(
        "\n---------------------------------\n\nPrompt",
        prompt_number + 1,
        "of",
        num_of_prompts,
        ":",
        prompts[prompt_number],
    )



# ----- END OF TESTS -----#

def main(num_story_per_topic, demonym, country_code, country_name):
    # Load the API key when the module is imported
    load_api_key()
    # Generate stories based on countries and save to CSV

    

    stories = generate_stories(num_story_per_topic, demonym, country_code, country_name)
    print(stories)
    dataset = create_dataset(stories, country_code)
    # time program execution
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    return dataset



if __name__ == "__main__":
    main()




    # countries = ["American", "Indian", "Nigerian", "Norwegian", "Australian", "Russian", "Ukrainian", "Israelian", "Palestinian", "Chinese"]
    
    # # Generate stories based on countries and save to CSV
    # for country in countries:
    #     stories = generate_stories([country], 100)
    #     dataset = create_dataset(stories, country)
    
