import os
import pandas as pd


def create_df(base_dir, data_type):
    """
  
    e.g. create_df("data", "names") will return a DataFrame with all names from the data directory

    """
    directories = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    
    # Start with an empty DataFrame
    combined_df = pd.DataFrame()

    for directory in directories:
        file_path = os.path.join(base_dir, directory, f"{directory}_{data_type}.csv")

        if os.path.exists(file_path):
            # Read CSV file
            data = pd.read_csv(file_path)
            
            # Identify the first two columns dynamically
            first_column = data.columns[0]  # Identifier (e.g., Name, Word, Sentiment)
            second_column = data.columns[1]  # Count column (or equivalent numeric measure)

            data[first_column] = data[first_column].astype(str)

            # Rename columns dynamically
            data = data[[first_column, second_column]].rename(columns={second_column: directory})
            print(data.head())
            # Merge with the existing DataFrame
            if combined_df.empty:
                combined_df = data
            else:
                combined_df = combined_df.merge(data, on=first_column, how="outer").fillna(0)

    print(combined_df.head())
    

    # Save to CSV
    output_file = f"analysis/data/combined_{data_type}.csv"
    combined_df.to_csv(output_file, index=False)

    print(f"✅ {output_file} created successfully!")
    
    return combined_df

if __name__ == "__main__":

    # create_df("data", "names")
    create_df("data", "noun_phrases")
    #create_df("data", "word_freq")


# Example usage:
# base_dir = "/path/to/country_directories"
# df = create_df(base_dir, "names")  # Works for names
# df = create_df(base_dir, "words")  # Works for words
# df = create_df(base_dir, "sentiment")  # Works for sentiment
# df = create_df(base_dir, "noun_phrases")  # Works for new file types!
# df = create_df(base_dir, "technology")  # Works for new file types!