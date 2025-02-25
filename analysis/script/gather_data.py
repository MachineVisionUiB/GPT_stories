import os
import pandas as pd


def create_df(base_dir, data_type):
    """
  
    e.g. create_df("data", "names") will return a DataFrame with all names from the data directory

    """
    
    
    # Start with an empty DataFrame
    combined_df = pd.DataFrame()


    if data_type == 'sentiments':
        dfs = []
        for directory in sorted(os.listdir(base_dir)):
            file_path = os.path.join(base_dir, directory, f"{directory}_sentiments.csv")

            if os.path.exists(file_path):
                # Read CSV file
                data = pd.read_csv(file_path)
                dfs.append(data)
                
        treshold = 0.85
        combined_df = count_high_scoring_sentiments(pd.concat(dfs), treshold)

    else:
        for directory in sorted(os.listdir(base_dir)):
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
    if not os.path.exists("analysis/data"):
        os.makedirs("analysis/data")
    output_file = f"analysis/data/combined_{data_type}.csv"
    combined_df.to_csv(output_file, index=False)

    print(f"✅ {output_file} created successfully!")
    
    return combined_df


def count_high_scoring_sentiments(input_df, threshold):
    """
    Count high-scoring sentiment entries in a single DataFrame and ensure all sentiment-country combinations have at least 0.
    """
    # Filter rows based on the confidence score threshold
    high_confidence = input_df[input_df['confidence'] >= threshold]

    # Get unique sentiments and countries
    all_sentiments = set(input_df['sentiment'].unique())
    all_countries = set(input_df['story_id'].str[:2].unique())

    high_confidence_dict = {sentiment: {country: 0 for country in all_countries} for sentiment in all_sentiments}

    # Count occurrences
    for index, row in high_confidence.iterrows():
        sentiment = row['sentiment']
        country = row['story_id'][:2]
        high_confidence_dict[sentiment][country] += 1

    # Convert to DataFrame and transpose
    df = pd.DataFrame.from_dict(high_confidence_dict, orient='index').fillna(0)
    
    # Reset index so 'country' is a column
    df.index.name = 'sentiment'
    df = df[sorted(df.columns)]
    df.reset_index(inplace=True)

    return df


def main():
    # Create a DataFrame for each type of data
    data_select = input("Enter the type of data you would like to analyze: \n1: word_freq\n2: noun_phrases\n3: names\n4: sentiments\n") # e.g., names, noun_phrases, word_freq, sentiments
    type_of_data = ''
    if data_select == "1":
        type_of_data = "word_freq"
    elif data_select == "2":
        type_of_data = "noun_phrases"
    elif data_select == "3":
        type_of_data = "names"
    elif data_select == "4":
        type_of_data = "sentiments"
    create_df("data", type_of_data)
    


if __name__ == "__main__":
    main()







# Example usage:
# base_dir = "/path/to/country_directories"
# df = create_df(base_dir, "names")  # Works for names
# df = create_df(base_dir, "words")  # Works for words
# df = create_df(base_dir, "sentiment")  # Works for sentiment
# df = create_df(base_dir, "noun_phrases")  # Works for new file types!
# df = create_df(base_dir, "technology")  # Works for new file types!