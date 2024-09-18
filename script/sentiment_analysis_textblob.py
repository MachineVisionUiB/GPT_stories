import pandas as pd
from textblob import TextBlob

# Load the CSV file
input_filename = input("Enter the input file name: ")+".csv"
df = pd.read_csv('/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/countries_samples_100words/'+input_filename)

# Function to get the sentiment (polarity and subjectivity)
def get_sentiment(text):
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    return polarity, subjectivity

# Apply sentiment analysis to the second column
df[['Polarity', 'Subjectivity']] = df.iloc[:, 1].apply(lambda x: pd.Series(get_sentiment(str(x))))

# Calculate the averages of the Polarity and Subjectivity columns
average_polarity = round(df['Polarity'].mean(), 2)
average_subjectivity = round(df['Subjectivity'].mean(), 2)

# Create a new DataFrame to hold the averages, using 'Average' as a label in the first column
average_row = pd.DataFrame({'Column1': ['Average'], 'Polarity': [average_polarity], 'Subjectivity': [average_subjectivity]})

# Append the average row to the original DataFrame
df_with_avg = pd.concat([df, average_row], ignore_index=True)

output_filename = input("Enter the output file name: ")+".csv"

# Save the modified file with the new columns and averages at the bottom
df_with_avg.to_csv(output_filename, index=False)



