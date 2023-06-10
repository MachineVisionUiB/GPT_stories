import os
import openai
import csv
from datetime import date



# Sets the key for the openai api
openai.api_key_path = "key.txt"

# Generates a message based on the marker
def generate_message(marker):
    vowels = ('a','e','i','o','u','A','E','I','O','U')
    article = ""
    if marker[0] in vowels:
        article = "an"
    else:
        article = "a"
    return f"Write a 50 word plot summary for {article} {marker} children's novel."

# Generates stories based on the user's input
def generate_stories():
    messages = [ {"role": "system", "content": ""} ]
    stories = []
    # The user has to specify a marker (American, British, etc.)
    message = generate_message(input("Enter a marker: "))
    # The user has to specify how many stories to generate
    n = int(input("Enter the number of stories to generate: "))
    # For loop that prompts chatgpt a specified number of times
    for i in range(n):
        messages.append({"role": "user", "content": message},)
        # Creates a chatgpt model based on the previous prompts and replies
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        # Removes the last prompt from the messages
        messages = messages[:-1]
        # A call to the chatgpt model that generates a reply
        reply = chat.choices[0].message.content
        # print(f"ChatGPT: {reply}")

        # Appends the prompt, reply, date, and modelname to the stories list
        unit = (message, reply, date.today(), "gpt-3.5-turbo") 
        stories.append(unit)
        
        
    return stories

# Generate stories
stories = generate_stories()


# Writes stories to a csv file
with open (f"{stories[0][0].split()[8]}_stories.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["prompt", "reply", "date" "modelname"])
    for story in stories:
        writer.writerow(story)




