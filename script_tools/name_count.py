import csv
from collections import Counter
import os
import re

def count_names(input_file, output_file):
    """
    Processes a CSV file to count occurrences of names from a specified column and saves the results to an output file.

    This function reads a CSV file, extracts names from the fifth column of each row, and counts their occurrences.
    Names are split based on commas, numbers followed by periods (e.g., "1. Earl"), or other non-alphanumeric symbols.
    The counts are then sorted in descending order and written to an output CSV file.

    Parameters
    ----------
    input_file : str
        Path to the input CSV file containing the names data.
    output_file : str
        Path to the output CSV file where name counts will be saved.

    Raises
    ------
    IOError
        If there is an issue reading from `input_file` or writing to `output_file`.

    Examples
    --------
    >>> count_names('input.csv', 'output.csv')
    This will read 'input.csv', count names from the fifth column, and save results to 'output.csv'.
    """
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

# Run the name counting function on the provided CSV files in a directory
directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/childrens_stories/full_stories_analysis/place_names'  # Replace with your directory path
for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    output_file = 'placename_counts_' + os.path.basename(os.path.normpath(f))
    if os.path.isfile(f):
        count_names(f, output_file)
        print(f"Name counts saved to {output_file}")
