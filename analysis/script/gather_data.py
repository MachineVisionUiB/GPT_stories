import os
import pandas as pd

def get_directory_names(base_dir):
    """
    Retrieves all directory names inside the given base directory.
    
    Args:
        base_dir (str): Path to the main directory.

    Returns:
        list: List of directory names.
    """
    directories = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    print("📂 Found Directories:", directories)  # Print the directory list
    
    return directories

def generate_filenames(directories, file_pattern):
    """
    Generates filenames dynamically based on directory names.

    Args:
        directories (list): List of directory names (e.g., country codes).
        file_pattern (str): Filename pattern using "{directory}" as a placeholder.

    Returns:
        dict: Mapping of directory names to expected filenames.
    """
    return {dir_name: file_pattern.format(directory=dir_name) for dir_name in directories}

    # Display result
    print("Combined Names Data:")
    print(output_names)

def fetch_data(base_dir, file_name_pattern, variable_name_in_file):
    """
    Reads a specific variable from CSV files in multiple subdirectories and
    combines them into a single DataFrame.

    Args:
        base_dir (str): Parent directory containing subdirectories (e.g., "data/").
        file_pattern (str): Filename pattern, e.g., "{directory}_names.csv".
        variable_name (str): Column containing values to merge (e.g., "Count").

    Returns:
        pd.DataFrame: A DataFrame where each row is a unique entity (e.g., Name)
                      and each directory has its own column with extracted values.
    """
    directory_names = get_directory_names(base_dir)
    filenames = generate_filenames(directory_names, file_pattern)
    combined_data = {}

    for directory, filename in filenames.items():
        file_path = os.path.join(base_dir, directory, filename)

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()  # Ensure column names are clean

            if variable_name in df.columns:
                combined_data[directory] = df.set_index(df.columns[0])[variable_name]
            else:
                print(f"⚠ Warning: '{variable_name}' not found in {file_path}. Available columns: {df.columns.tolist()}")


    # Merge all data into a single DataFrame
    result_df = pd.DataFrame(combined_data).fillna(0)  # Replace NaN with 0
    result_df.columns = [f"{col}-count" for col in result_df.columns]  # Rename columns

    return result_df



if __name__ == "__main__":
    
    base_directory = "data"  # Parent directory where subdirectories exist

    output_names = fetch_data(base_directory, "{directory}_names.csv", "Count")
    print("Combined Names Data:")
    print(output_names)  # Add this line to see the result

    file_patterns = [
        "{directory}_names.csv",
        "{directory}_word_freq.csv",
        "{directory}_summaries_100.csv",
        "{directory}_noun_phrases.csv",
        "{directory}_stories.csv"
        ]

