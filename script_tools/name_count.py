import csv
from collections import Counter
import os

def count_names(input_file, output_file):
    # Read names from the 5th column of the input CSV file
    names = []
    with open(input_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if it exists
        for row in reader:
            if len(row) >= 5:
                names.append(row[4])  # Append the name from the 5th column

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

directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/full_stories_analysis/main_char'
for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    output_file = 'name_counts_' + os.path.basename(os.path.normpath(f))
    if os.path.isfile(f):
        count_names(f, output_file)


