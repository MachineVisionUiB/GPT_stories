import csv
import os

def csv_to_txt(input_csv, output_txt):
    with open(input_csv, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip the header row

        with open(output_txt, 'w', encoding='utf-8') as txtfile:
            for i, row in enumerate(reader):
                if i >= 10:  # Stop after the first 10 rows
                    break
                
                story_id = row[0]
                story = row[1]
                summary = row[4]
                
                # Write each section clearly separated
                txtfile.write(f"Story ID: {story_id}\n\n")
                txtfile.write(f"Story:\n{story}\n\n\n")
                txtfile.write(f"Summary:\n{summary}")
                txtfile.write("\n\n\n" + ("-" * 40) + "\n\n\n")  # Separator for readability

    print(f"Data from the first 10 rows of {input_csv} has been written to {output_txt}.")



# Use the function
directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/summaries' # Replace with your directory path
for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        output_txt = '10_' + (filename.replace('.csv', '.txt')).replace('summary_', '')
        csv_to_txt(f, output_txt)

