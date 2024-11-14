import csv
import os
from collections import Counter

def count_high_scoring_sentiments(input_dir, output_file):
    # Prepare to write the output CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Sentiment', 'Count'])

        # Process each file in the directory
        for filename in os.listdir(input_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(input_dir, filename)
                sentiment_counts = Counter()

                # Read the input CSV file
                with open(filepath, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header row if present

                    # Process each row in the current file
                    for row in reader:
                        sentiment = row[5]
                        score = float(row[6])
                        if score >= 0.85: # Adjust the threshold as needed
                            sentiment_counts[sentiment] += 1

                # Write the file name and sentiment counts to the output CSV
                writer.writerow([filename])  # File name header
                for sentiment, count in sentiment_counts.items():
                    writer.writerow(['', sentiment, count])  # Empty first column for clarity

# Example usage
input_dir = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/summaries_analysis/hf_sentiment'  # Replace with your input directory path
output_file = 'hf_sentiment_count.csv'  # Replace with your desired output file name
count_high_scoring_sentiments(input_dir, output_file)
