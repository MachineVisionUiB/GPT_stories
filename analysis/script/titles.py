import pandas as pd

"""
This is an unelegant way to get lists of titles for different countries,
and to count how many titles contain certain words. Sorry about the mess. To
use you will have to edit the code directly but hopefully it's easy to see how.
- Jill
"""

stories = pd.read_csv("data/US/US_stories.csv")

#find all strings that start with "**Title:" and end with "**" in the column "Story" and extract the text in between
titles = stories["Story"].str.extract(r"\*\*Title: (.*?)\*\*")
print(titles)

# how many titles include the word train
train_count = titles[0].str.contains("train", case=False, na=False).sum()
print(f"Number of titles that include the word 'train': {train_count}")

home_count = titles[0].str.contains("home", case=False, na=False).sum()
print(f"Number of titles that include the word 'home': {home_count}")

#same for wood
wood_count = titles[0].str.contains("wood", case=False, na=False).sum()
print(f"Number of titles that include the word 'wood': {wood_count}")

#same for Whispering
whispering_count = titles[0].str.contains("Whispering", case=False, na=False).sum()
print(f"Number of titles that include the word 'Whispering': {whispering_count}")

#same for Pines
pines_count = titles[0].str.contains("Pines", case=False, na=False).sum()
print(f"Number of titles that include the word 'Pines': {pines_count}")

#same for Fjord
fjord_count = titles[0].str.contains("Fjord", case=False, na=False).sum()
print(f"Number of titles that include the word 'Fjord': {fjord_count}")

# for Maplewood
maplewood_count = titles[0].str.contains("Maplewood", case=False, na=False).sum()
print(f"Number of titles that include the word 'Maplewood': {maplewood_count}")

# list all titles containing the word with the string whisper or echo or secret
whisper_titles = titles[titles[0].str.contains("whisper", case=False, na=False)]
print("There are ",len(whisper_titles), " titles with the word whisper, echo or secret: ", whisper_titles)

titles["count"] = titles.groupby(0)[0].transform('count')
#sort by count
titles = titles.sort_values(by="count", ascending=False)
#drop duplicates
titles = titles.drop_duplicates(subset=0)

#list all titles that include the word "train"
train_titles = titles[titles[0].str.contains("train", case=False, na=False)]
print(train_titles)

#list the titles that are NOT in train_titles wiht a count
other_titles = titles[~titles[0].isin(train_titles[0])]
print(other_titles)

# Create a list of other_titles without the count and with no quotation marks, just as comma-separated text
other_titles_list = other_titles[0].dropna().tolist()  # Drop NaN values
other_titles_str = ", ".join(map(str, other_titles_list))  # Convert all elements to strings
print(other_titles_str)

""" #make wordcloud from titles
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(" ".join(titles[0].dropna()))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
 """