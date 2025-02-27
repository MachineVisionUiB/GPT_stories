import os
import pandas as pd

def gather_sentiment_data(base_dir, output_file):
    """ 
    Reads all sentiment files from country directories, extracts story_id, sentiment, and confidence, 
    and combines them into a single CSV file.
    """

    all_data = []

    for directory in sorted(os.listdir(base_dir)):
        file_path = os.path.join(base_dir, directory, f"{directory}_sentiments.csv")

        if os.path.exists(file_path):
            # Read CSV file, ensuring necessary columns exist
            try:
                data = pd.read_csv(file_path, usecols=['story_id', 'sentiment', 'confidence'])
                data['alpha-2'] = directory  # Add country column for reference
                all_data.append(data)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Combine all data into a single DataFrame
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)

    else:
        print("No sentiment files found.")
    
    country_data = pd.read_csv("support_data/country_data.csv")
    # merge data with country_data
    combined_df = pd.merge(combined_df, country_data, on='alpha-2', how='left')

    # Change the value "United States of America (the)" to "USA"
    # add replacements for Bolivia (Plurinational State of), United Kingdom of Great Britain and Northern Ireland (the), Korea (the Republic of), Korea (the Democratic People's Republic of)
    combined_df['country_name'] = combined_df['country_name'].replace({
        "United States of America (the)": "USA",
        "Palestine, State of": "Palestine",
        "United Kingdom of Great Britain and Northern Ireland (the)": "United Kingdom",
        "Korea (the Republic of)": "South Korea",
        "Korea (the Democratic People's Republic of)": "North Korea",
        "Bolivia (Plurinational State of)": "Bolivia",
        "Taiwan (Province of China)": "Taiwan",
        "Russian Federation (the)": "Russia",
        "Iran (Islamic Republic of)": "Iran",
        "Venezuela (Bolivarian Republic of)": "Venezuela",
    })

    combined_df.to_csv(output_file, index=False)
    print(f"Combined sentiment data saved to {output_file}")



# Example usage:
gather_sentiment_data("data", "analysis/data/all_countries_sentiments.csv")
