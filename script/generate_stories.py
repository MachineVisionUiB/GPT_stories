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

    [more explanation of the module]
 
    """
import os
import openai
#import pandas as pd

with open('key.txt', 'r') as file:
    openai.api_key = file.readline().strip()


def create_stories_data_frame():
    pass

def generate_plots(topics: list[str], number_of_plots_per_topic: int):
    """
    Generates a prompt for each item in the topics list, then sends each 
    prompt to the OpenAI API to generate a plot summary as many times as
    specified by the number_of_plots_per_topic parameter. 
    
    The basic structure of the prompt is "Write a 50 word plot summary for a 
    potential [topic] children's novel." The generated plot summaries are saved to a pandas
    dataframe.

    Parameters
    ----------
    topics : list[str]
        A list of topics, e.g. cultures or countries. A prompt will be
        generated for each item in the list.
    number_of_plots_per_topic : int
        The number of plots to generate for each topic.

    Returns
    -------
    int
        A pandas dataframe containing the generated plots.

    Examples
    --------
    >>> generate_plots(["Native American", "Asian American"], 2)

    >>> generate_plots(["Norwegian", "Australian"], 3)
    
    """
    prompts = make_prompts(topics)
    for prompt_number in range(len(prompts)):
        print("Prompt number ", prompt_number, prompts[prompt_number])
        for prompt_iteration in range(number_of_plots_per_topic):
            print("Iteration number", prompt_iteration, prompts[prompt_number])


        # story = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=make_prompts(cultures),
        #     temperature=0.6,
        #     n=n,
        #     max_tokens=70,
        #     )
   
    
def make_prompts(topics):
    """Makes a prompt for the story generation.
    """
    prompts = []
    try:
        for topic in topics:
            prompt = f"Write a 50 word plot summary for a potential {topic} children's novel."
            prompts.append(prompt)
        print(prompts)
    except: print("Error: topics must be a list of strings.")
    return prompts

def test_make_prompts():
    topics = ["Native American", "Asian American"]
    prompts = make_prompts(topics)
    assert prompts[0] == "Write a 50 word plot summary for a potential Native American children's novel."
    assert prompts[1] == "Write a 50 word plot summary for a potential Asian American children's novel."



if __name__ == "__main__":
    
    cultures = ["Native American", "Asian American", "African American", "Latinx", "Middle Eastern", "South Asian", "East Asian", "Pacific Islander", "Indigenous Australian", "Indigenous Canadian", "Indigenous Mexican", "Indigenous South American", "Indigenous Central American"]
    countries = ["Norwegian", "Australian"]

    #make_prompts(cultures)
    # make_prompts("silly")

    generate_plots(cultures,40)