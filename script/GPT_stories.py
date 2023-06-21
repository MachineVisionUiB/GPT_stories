import os
import openai
import csv
from datetime import date

# Sets the key for the openai api. You need to refer to the path where you saved your key.txt file
openai.api_key_path = "key.txt"


#  this function gives context to GPT and returns the list of messages
def initiate_chat():
    messages = [{"role": "system", "content": ""}]

    # example 1
    # prompt
    messages.append({"role": "user", "content": """Read the following plot summary of a fictional children's story. Then do five things. \
1: State the place in which the story takes place. \n\
2: State the name of the main character. \n \
3: Does the protagonist save something from a threat? Who or what is saved, and what is that threat? \n \
4: Reason step by step to decide what character traits are most valued in this story. \
Choose a single word to describe each character trait. Each story has between one and three valued character traits. Do not say zero or N/A.\n \
5: List the character traits, separated by commas.
6: Given the amount of speculation required in step 3, describe your certainty about the estimate--either high, moderate, or low.\n \
The passage follows:\n \
"In the heart of Lagos, twelve-year-old Amina discovers a magical book hidden in her grandfather's library. With the help of a mischievous talking parrot, she embarks on a thrilling adventure through Nigerian folklore to save her village from a vengeful spirit, discovering her own courage and heritage along the way."""})
    # reply
    messages.append({"role": "assistant", "content": 
"""1:Lagos \n\
2: Amina \n\
3: Amina saves her village from a vengeful spirit. \n \
4: The summary states that the protagonist discovers her own courage and heritage along the way, so the valued character traits are courage and heritage. I'm not quite sure whether heritage is a character trait.\n\
5: courage, heritage \n\
6: Moderate confidence."""
})
    

    # example 2
    # prompt
    messages.append({"role": "user", "content": """Read the following plot summary of a fictional children's story. Then do five things. \
1: State the place in which the story takes place. \n\
2: State the name of the protagonist. \n \
3: Does the protagonist save something from a threat? Who or what is saved, and what is that threat? \n \
4: Reason step by step to decide what character traits are most valued in this story. \
Choose a single word to describe each character trait. Each story has between one and three valued character traits. Do not say zero or N/A.\n \
5: List the character traits, separated by commas.
6: Given the amount of speculation required in step 3, describe your certainty about the estimate--either high, moderate, or low.\n \
The passage follows:\n \
"In the small town of Willowville, young Emma discovers a hidden portal to a magical world. With her newfound friends, a talking squirrel and a mischievous pixie, she embarks on an adventure to save the enchanted creatures from an ancient curse. Together, they learn the power of friendship and bravery."""})
    # reply
    messages.append({"role": "assistant", "content": """1: Willowville \n\
2: Emma \n\
3: Emma saves the enchanted creatures from an ancient curse. \n \
4: The characters learn the power of friendship and bravery, so friendship and bravery are valued strongly in this story.\n\
5: friendship, bravery \n\
6: High confidence."""
})
    
    # example 3
    # prompt
    messages.append({"role": "user", "content": """Read the following plot summary of a fictional children's story. Then do five things. \
1: State the place in which the story takes place. \n\
2: State the name of the main character. \n \
3: Does the protagonist save something from a threat? Who or what is saved, and what is that threat? \n \
4: Reason step by step to decide what character traits are most valued in this story. \
Choose a single word to describe each character trait. Each story has between one and three valued character traits. Do not say zero or N/A.\n \
5: List the character traits, separated by commas.
6: Given the amount of speculation required in step 3, describe your certainty about the estimate--either high, moderate, or low.\n \
The passage follows:\n \
""In 'The Secret of the Northern Lights', young Sven and Freya embark on an enchanting journey through the Norwegian wilderness. With a mystical map, an ancient legend, and their own courage, they seek the hidden heart of the auroras, hoping to restore harmony to their village and the Northern Lights."""})
    # reply
    messages.append({"role": "assistant", "content": """1: The Norwegian wilderness \n\
2: Sven and Freya \n\
3: Sven and Freya restore harmony to their village and the Northern Lights, so the thing (or place in this case) that is under threat is their village and the Northern Lights. The plot summary doesn't say what is threatening the village and the Northen lights. \n \
4: The summary states that the protagonist discovers her own courage and heritage along the way, so the valued character traits are courage and heritage. I'm not quite sure whether heritage is a character trait.\n\
5: courage, heritage \n\
6: Moderate confidence."""})

    return messages


# analyses stories from input file and writes results to output file
def analyze(messages, stories):
    with open (stories, "r", encoding="utf8") as f:
        read_stories = csv.reader(f, delimiter=";")
        next(read_stories, None)
        for i, line in enumerate(read_stories):
            # adding story to messages
            messages.append({"role": "user", "content": line[1]})
            try:
                # creating chat
                chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                reply = chat.choices[0].message.content
                # splitting reply into separate lines
                reply = reply.split("\n")
                unit = {"prompt": line[1], "location": reply[0], "main_char": reply[1], "save": reply[2], "char_t_reason": reply[3], "char_t": reply[4], "certainty": reply[5], "date": date.today(), "modelname": "gpt-3.5-turbo"}
            except:
                print("An error occured. The program continues.")
                messages = messages[:-1]
                analyze(messages, stories[i:])
               
            # writing to output file
            with open ("output.csv", "a", encoding="utf8", newline='') as g:
                writer = csv.DictWriter(g, delimiter=";", fieldnames=["prompt", "location", "main_char", "save", "char_t_reason", "char_t", "certainty", "date", "modelname"])
                # if file is empty, write header
                if os.stat("output.csv").st_size == 0:
                    writer.writeheader()

                
                writer.writerow(unit)
                # removes the last message from the list. This is necessary so that the last message doesn't affect the following analysis
                messages = messages[:-1]


# prompts user to create or analyze stories
def create_or_analyze():
    while True:
        choice = input("Do you want to create a new story or analyze an existing one? (c=create/a=analyze): ")
        if choice.lower() == "c":
            return True
        elif choice.lower() == "a":
            return False
        else:
            print("Please enter either 'y' or 'n'")


# The user has to specify the number of stories to generate
def num_stories():
    while True:
        n = int(input("Enter the number of stories to generate: "))
        # check if n is an integer
        if isinstance(n, int):
            break
        else:
            print("Please enter an integer")
    return n
    
# The user has to specify a category (American, British, etc.)
def category():
    category = input("Enter a category: ")
    return category

# message = generate_message(category)
def message(category):
    message = f"Write a 50 word plot summary for a potential {category} children's novel."
    return message


# The user has to speficy the language
def language():
    language = input("Enter a language: ")
    return language

# The user has to specify the output filename
def filename():
    filename = input("Enter the output filename: ")
    return filename + ".csv"

# The user has to specify the temperature
def temperature():
    while True:
        temp = float(input("Enter the temperature: "))
        # check if temp is a float and between 0 and 1
        if isinstance(temp, float) and temp > 0 and temp <= 1:
            break
        else:
            print("Please enter a float between 0 and 1")
    return temp

# Generates a single story based on the user's input
def generate_story(message, language, category, filename, temp):
    messages = [{"role": "system", "content": ""}]
    messages.append({"role": "user", "content": message})

    try:
        # Create a chatgpt model based on the previous prompts and replies
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature=temp)
        reply = chat.choices[0].message.content
        unit = {"prompt": message, "reply": reply, "date": date.today(), "modelname": "gpt-3.5-turbo",
                "temperature": temp, "language": language, "culture": category}

        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=["prompt", "reply", "date", "modelname",
                                                                  "temperature", "language", "culture", "country"])
            if os.stat(filename).st_size == 0:
                writer.writeheader()
            writer.writerow(unit)

    except:
        print("An error occurred")
        generate_story(message, language, category, filename, temp)


# Generates stories based on the user's input and writes them to a CSV file
def generate_stories(num_of_stories, message, language, category, filename, temp):
    for i in range(num_of_stories):
        generate_story(message, language, category, filename, temp)


def main():
    if create_or_analyze():
        cat = category()
        num_of_stories = num_stories()
        lan = language()
        # to use the message function, uncomment the following line, and comment the next one
        mes = message(cat)
        # to have a specific message, uncomment the following line, write your message, and comment the previous one
        mes = ""
        temp = temperature()
        fil = filename()
        generate_stories(num_of_stories, mes, lan, cat, fil, temp)
    else:
        chat = initiate_chat()
        stories = input("Enter the name of the file containing the stories: ")
        analyze(chat, stories)


# Calls the main function
if __name__ == "__main__":
    main()






