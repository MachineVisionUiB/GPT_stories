import os
import openai
import pandas as pd
from dotenv import load_dotenv
import csv


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




def generate_stories(topics: list[str], number_of_stories_per_topic: int):
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
    word_count = 100
    prompts = make_prompts(topics, word_count)  # Generate prompts based on topics
    stories = []

    # Print initial statement about prompts and stories to be generated
    prompt_init_print(prompts, number_of_stories_per_topic)

    for prompt_number in range(len(prompts)):
        # Print details of the current prompt and prompt count
        prompt_counter_print(prompts, prompt_number)

        for story_iteration in range(number_of_stories_per_topic):
            messages = [{"role": "system", "content": ""}]  # Initial system message
            messages.append({"role": "user", "content": prompts[prompt_number]})
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.8,
                n=1,
            )
            # Extract generated story from the response
            story = response.choices[0].message.content
            # Create a unique identifier for each story
            story_id = f"{topics[prompt_number]}_{story_iteration+1}"
            stories.append((story_id, story, prompts[prompt_number], topics[prompt_number]))
            # Print the generated story
            print(f"\nVersion {story_iteration+1}: {story}")

    return stories


def create_dataset(stories, country):
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
    df = pd.DataFrame(stories, columns=['Story ID', 'Story', 'Prompt', 'Topic'])

    # Generate a unique filename from user input
    filename =  country + "_children_stories.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)

    print(f"Dataset saved to {filename}")

    return df


def make_prompts(topics, word_count):
    """
    Generates a list of prompts based on a list of topics.

    For each topic in the list, this function creates a prompt asking for a
    story, or a children's story of a specific word count.

    Parameters
    ----------
    topics : list[str]
        A list of topics, such as countries or cultures.
    word_count : int
        The word count for the plot summary.

    Returns
    -------
    list
        A list of generated prompts.
    """
    prompts = []
    try:
        for topic in topics:
            prompt = f"Write a {word_count} word potential {topic} novel."
            prompts.append(prompt)
        print("\n", len(prompts), "unique prompts generated.\n")
    except:
        print("Error: topics must be a list of strings.")
    return prompts


def prompt_init_print(prompts, number_of_stories_per_topic):
    """
    Prints the number of unique prompts and the number of stories per prompt.

    Parameters
    ----------
    prompts : list
        A list of generated prompts.
    number_of_stories_per_topic : int
        The number of stories to generate for each prompt.
    """
    print(
        "Sending",
        len(prompts),
        "unique prompts to the OpenAI API, and generating",
        number_of_stories_per_topic,
        "stories for each prompt.",
    )


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


# ----- TESTS -----#


def test_make_prompts():
    """
    Unit test for the make_prompts function.
    """
    topics = ["Native American", "Asian American"]
    prompts = make_prompts(topics, 50)
    assert (
        prompts[0]
        == "Write a 50 word plot summary for a potential Native American children's novel."
    )
    assert (
        prompts[1]
        == "Write a 50 word plot summary for a potential Asian American children's novel."
    )


# ----- END OF TESTS -----#

def main(countries, num_story_per_topic):
    # Load the API key when the module is imported
    load_api_key()
    # Generate stories based on countries and save to CSV
    country_datasets = []
    for country in countries:
        stories = generate_stories([country], num_story_per_topic)
        dataset = create_dataset(stories, country)
        country_datasets.append(dataset)
    print(country_datasets)
    return country_datasets



if __name__ == "__main__":
    main()




    # countries = ["American", "Indian", "Nigerian", "Norwegian", "Australian", "Russian", "Ukrainian", "Israelian", "Palestinian", "Chinese"]
    
    # # Generate stories based on countries and save to CSV
    # for country in countries:
    #     stories = generate_stories([country], 100)
    #     dataset = create_dataset(stories, country)
    
