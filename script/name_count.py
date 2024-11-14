import csv
from collections import Counter
import os
import re

def count_names(input_file, output_file):
    # List to store individual names
    names = []

    with open(input_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if it exists
        for row in reader:
            if len(row) >= 5:
                # Get the raw string from the 5th column
                raw_names = row[4]

                # Split the string based on different delimiters:
                # - comma
                # - numbers followed by a period (like "1. Earl")
                # - any other non-alphanumeric symbols (generalized)
                split_names = re.split(r',|\d+\.\s*|[^a-zA-Z\s]+', raw_names)

                # Clean up extra whitespace and filter out any empty strings
                split_names = [name.strip() for name in split_names if name.strip()]

                # Extend the names list with these individual names
                names.extend(split_names)

    # Count occurrences of each name
    name_counts = Counter(names)

    # Sort names by count in descending order
    sorted_name_counts = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)

    # Write the counts to the output CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'count'])
        for name, count in sorted_name_counts:
            writer.writerow([name, count])

# Example usage
directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/full_stories_analysis/place_names'
for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    output_file = 'placename_counts_' + os.path.basename(os.path.normpath(f))
    if os.path.isfile(f):
        count_names(f, output_file)
        print(f"Name counts saved to {output_file}")