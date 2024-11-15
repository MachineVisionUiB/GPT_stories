import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
file_path = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/summaries_analysis/hf_sentiment/hf_sentiment_count_85.csv'
df = pd.read_csv(file_path)

# Ensure country names are strings and convert sentiment columns to numeric, filling NaNs with 0
df.iloc[:, 0] = df.iloc[:, 0].astype(str)  # Convert countries to strings
df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').fillna(0)  # Convert to numeric and fill NaNs

# Extract country names and sentiment counts
countries = df.iloc[:, 0]  # First column with country names
sentiments = df.columns[1:]  # All columns after the first are sentiment types
sentiment_counts = df.iloc[:, 1:]  # All rows for sentiment data

# Define the number of countries and sentiments
num_countries = len(countries)
num_sentiments = len(sentiments)

# Define the position and width of bars
x = np.arange(num_countries)  # label locations
width = 0.2  # width of each bar

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each sentiment as a bar set
for i, sentiment in enumerate(sentiments):
    ax.bar(x + i * width, sentiment_counts[sentiment], width, label=sentiment)

# Add labels, title, and custom x-axis tick labels
ax.set_xlabel('Country')
ax.set_ylabel('Sentiment Count')
ax.set_title('Sentiment Distribution by Country')
ax.set_xticks(x + width * (num_sentiments - 1) / 2)
ax.set_xticklabels(countries, rotation=45, ha="right")
ax.legend(title="Sentiments")

plt.tight_layout()
plt.show()
