import os
import pandas as pd

base_dir = "data" 

directories = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
output = pd.DataFrame(columns=["Name"])

for directory in directories:
    file_path = os.path.join(base_dir, directory, f"{directory}_names.csv")

    if os.path.exists(file_path):
        # fetch data from Name and Count variables. rename Count to {directory}
        data = pd.read_csv(file_path)
        data = data[["Name", "Count"]].rename(columns={"Count": directory})
        # for the next iteration, merge the data with the previous data
        if "output" in locals():
            output = output.merge(data, on="Name", how="outer").fillna(0)
        else:
            output = data

#output.to_csv(f"analysis/data/global_names_count.csv", index=False)

count_columns = output.columns[1:] 
# Calculate proportions by dividing each value by the sum of its column (country)
output[count_columns] = output[count_columns].div(output[count_columns].sum(axis=0), axis=1)

#output.to_csv(f"analysis/data/global_names_proportion.csv", index=False)

#filter out names that are not in at least 20% of the countries
output = output[output[count_columns].gt(0.5).any(axis=1)]
print(output)




if __name__ == "__main__":
    
    base_directory = "data"  # Parent directory where subdirectories exist

    #output_names = fetch_data(base_directory, "{directory}_names.csv", "Count")
    #print("Combined Names Data:")
    #print(output_names)  # Add this line to see the result

    file_patterns = [
        "{directory}_names.csv",
        "{directory}_word_freq.csv",
        "{directory}_summaries_100.csv",
        "{directory}_noun_phrases.csv",
        "{directory}_stories.csv"
        ]

