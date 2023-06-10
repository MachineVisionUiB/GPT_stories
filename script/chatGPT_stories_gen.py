import os
import openai
import csv
from datetime import date

# Sets the key for the openai api. You need to refer to the path where you saved your key.txt file
openai.api_key_path = "key.txt"

# Generates a message based on the marker
def generate_message(category):
    vowels = ('a','e','i','o','u','A','E','I','O','U')
    article = ""
    if category[0] in vowels:
        article = "an"
    else:
        article = "a"
    return f"Write a 50 word plot summary for {article} {category} children's novel."

# Generates stories based on the user's input and writes them to a csv file
def generate_stories():
    messages = [ {"role": "system", "content": ""} ]
    # The user has to specify a category (American, British, etc.)
    category = input("Enter a marker: ")
    message = generate_message(category)
    # The user has to specify how many stories to generate
    n = int(input("Enter the number of stories to generate: "))
    # For loop that prompts chatgpt a specified number of times and for each iteration writes the prompt, reply, date and model to a csv file
    for i in range(n):
        with open (f"{category}_stories.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=["prompt", "reply", "date", "modelname"])
            # If the file is empty, it writes the fieldnames
            if os.stat(f"{category}_stories.csv").st_size == 0:
                writer.writeheader()
            messages.append({"role": "user", "content": message},)
            # Creates a chatgpt model based on the previous prompts and replies
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            # Removes the last prompt from the messages
            messages = messages[:-1]
            # A call to the chatgpt model that generates a reply
            reply = chat.choices[0].message.content
            unit = {"prompt": message, "reply": reply, "date": date.today(), "modelname": "gpt-3.5-turbo"}
            # writes the prompt, reply, date and model to a csv file
            writer.writerow(unit)
            

# Generate stories
stories = generate_stories()







