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
 
    """
import os
import openai
#import pandas as pd

with open('key.txt', 'r') as file:
    openai.api_key = file.readline().strip()


def create_stories_data_frame():
    pass

def generate_plots(num_plots=5, topics): # need for loops for num_plots and topics  
        # story = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=make_prompts(cultures),
        #     temperature=0.6,
        #     n=3,
        #     max_tokens=70,
        #     )
   
def plots_for_each_topic_loop():
    pass


    
def make_prompts(topics):
    """Makes a prompt for the story generation.
    """
    prompts = []
    if type(topics) != list:
        print("Error: topics must be a list.")
    else:
        for topic in topics:
            prompt = f"Write a 50 word plot summary for a potential {topic} children's novel."
            prompts.append(prompt)
        print(prompts)
    return prompts

def test_make_prompts():
    topics = ["Native American", "Asian American"]
    prompts = make_prompts(topics)
    assert prompts[0] == "Write a 50 word plot summary for a potential Native American children's novel."
    assert prompts[1] == "Write a 50 word plot summary for a potential Asian American children's novel."



if __name__ == "__main__":
    
    cultures = ["Native American", "Asian American"]
    countries = ["Norwegian", "Australian"]

    #make_prompts(cultures)
    #make_prompts("silly")

    generate_plots()