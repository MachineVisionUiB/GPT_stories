"""
    Calls the OpenAI API to generate short plot summaries and 
    save them to a csv file.

    The OpenAI API key must be saved as the first line of a plain text file 
    called key.txt. The first two lines after the libraries are imported reads
    the first line of key.txt, strips any whitespace, and sets it as the API 
    key. If you fork this repo, make sure never to commit your key.txt file to
    GitHub or a public repository - it should be in your .gitignore file. You
    should also make sure to set your maximum usage of tokens at the OpenAI site
    to an amount you can afford.

    The generate_stories function sends prompts to the OpenAI and requests a 
    plot summary as many times as specified.

    Only one prompt is sent to the model at a time, and no history is retained.
    This means that each story iteration is generated as though from a blank 
    slate, without knowledge of previous prompts or previously generated stories.

    [more explanation of the module]
 
    """
import os
import openai
import pandas as pd
from dotenv import load_dotenv
import sys


# Set the API key for OpenAI
with open ("api_key.txt", "r") as f:
    openai.api_key = f.read().strip()

def generate_stories(topics: list[str], number_of_stories_per_topic: int):
    """
    Generates a prompt for each item in the topics list, then sends each
    prompt to the OpenAI API to generate a plot summary as many times as
    specified by the number_of_stories_per_topic parameter.

    The basic structure of the prompt is "Write a 50 word plot summary for a
    potential [topic] children's novel." The generated plot summaries are saved to a pandas
    dataframe.

    I use the term "story" instead of "plot" in the code to avoid confusion with the
    plotting of data.

    Parameters
    ----------
    topics : list[str]
        A list of topics, e.g. cultures or countries. A prompt will be
        generated for each item in the list.
    number_of_stories_per_topic : int
        The number of plots to generate for each topic.

    Returns !!!!FINISH THIS LATER!!!!
    -------
    int
        A pandas dataframe containing the generated plots.

    Examples
    --------
    >>> generate_plots(["Native American", "Asian American"], 2)

    >>> generate_plots(["Norwegian", "Australian"], 3)

    """
    messages = [{"role": "system", "content": ""}]
    prompts = make_prompts(topics)
    print(
        "Sending",
        len(prompts),
        "unique prompts to the OpenAI API, and generating",
        number_of_stories_per_topic,
        "stories for each prompt.",
    )
    for prompt_number in range(len(prompts)):
        print(
            "\n---------------------------------\nPrompt",
            prompt_number,
            "of",
            len(prompts),
            ":",
            prompts[prompt_number],
        )
        for story_iteration in range(number_of_stories_per_topic):
            messages.append({"role": "user", "content": prompts[prompt_number]})
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1,
                n=1,
            )
            # Extract the generated story from the response
            story = response.choices[0].message.content

            # Print the version and story
            print(f"\nVersion {story_iteration}: {story}")
            
    print(
        "\n--------------------------",
        "\nThat's it.\nThe next version of this program will save the output as a csv file.",
    )


def make_prompts(topics):
    """
    Makes a prompt for the story generation.
    """
    prompts = []
    try:
        for topic in topics:
            prompt = f"Write a 50 word plot summary for a potential {topic} children's novel."
            prompts.append(prompt)
        print("\n", len(prompts), "unique prompts generated.\n")
    except:
        print("Error: topics must be a list of strings.")
    return prompts


def save_stories(stories):
    pass


# ----- TESTS -----#


def test_make_prompts():
    topics = ["Native American", "Asian American"]
    prompts = make_prompts(topics)
    assert (
        prompts[0]
        == "Write a 50 word plot summary for a potential Native American children's novel."
    )
    assert (
        prompts[1]
        == "Write a 50 word plot summary for a potential Asian American children's novel."
    )


# ----- END OF TESTS -----#

if __name__ == "__main__":
    cultures = ["Native American", "Asian American"]
    # cultures = ["Native American", "Asian American", "African American", "Latinx", "Middle Eastern", "South Asian", "East Asian", "Pacific Islander", "Indigenous Australian", "Indigenous Canadian", "Indigenous Mexican", "Indigenous South American", "Indigenous Central American"]
    # countries = ["Norwegian", "Australian"]
    countries = [
        "Indian",
        
    ]

    # make_prompts(cultures)
    # make_prompts("silly")

    generate_stories(countries, 4)
