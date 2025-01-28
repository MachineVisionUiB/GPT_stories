import pandas as pd
import matplotlib.pyplot as plt
# Description: Visualise the most unique words per country

import os
print(os.getcwd())

# Load the data
data = pd.read_csv('most_unique_words_per_country.csv')

# Set pandas to display all rows (useful for testing)
pd.set_option('display.max_rows', None)

data['diff'] = data['frequency'] - data['uniqueness_score']
data['proportion_of_global'] = data['uniqueness_score'] / data['frequency']
#filtered_data = data[data['diff'] > 0]
#sorted_data = filtered_data.sort_values(by='unique_prop', ascending=False)
#print(sorted_data)

# Fetch country names and alpha-3 codes from the country code dataset and merge with the data
country_code_dataset_URL = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/refs/heads/master/all/all.csv'
codes = pd.read_csv(country_code_dataset_URL, usecols=['alpha-2', 'name', 'alpha-3', 'region', 'sub-region'])
data = pd.merge(data, codes, left_on='Country', right_on='alpha-2', how='left')

# Fetch population numbers from the World Bank dataset and merge into the data
population = pd.read_csv(
    'support_data/World_Bank_population_numbers.csv', 
    usecols=['Country Code', '2023'], 
    skiprows=4
    )

# Set pandas to display floats in standard notation
pd.options.display.float_format = '{:,.0f}'.format

data = pd.merge(
    data, 
    population, 
    left_on='alpha-3', 
    right_on='Country Code', 
    how='left')

data.rename(columns={'2023': 'population'}, inplace=True)

# remove unnecessary columns
#data = data.drop(columns=['Country Code'])

print(data.head())
print(data.columns)


# Display the merged data
print("Data loaded, will now visualise the data")

# Save the data to a CSV file
data.to_csv('data/unique_words_by_country_expanded.csv', index=False)

# -------------------Testing  Visualisation ------------------- 

# All the countries where word frequency is greater than 1000 have stop words 
# in the local language as most unique word, so filter them out.

data = data[data['frequency'] < 1000]

plt.figure(figsize=(10, 6))
plt.scatter(data['population'], data['frequency'], alpha=0.7, edgecolors='k')
plt.title('Relationship Between Pop and fre', fontsize=14)
plt.xlabel('population', fontsize=12)
plt.ylabel('freq', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Add labels for each point
for i, row in data.iterrows():
    label = f"{row['name']} ({row['word']})" 
    plt.text(row['population'], row['frequency'], label, fontsize=8, ha='right', va='bottom', alpha=0.7)

plt.tight_layout()
plt.show()

exit()


# ------------------- Visualisation -------------------

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(data_cleaned['2023'], data_cleaned['proportion_of_global'], alpha=0.7, edgecolors='k')

# Add labels for only extreme values to reduce clutter
for i, row in data_cleaned.iterrows():
    if row['proportion_of_global'] > 0.9 or row['2023'] > 1e8:  # Apply filtering row by row
        label = f"{row['name']} ({row['word']})"  # Format as "Country (Word)"
        plt.text(row['2023'], row['proportion_of_global'], label, 
                 fontsize=row['scaled_font_size'], ha='right', va='bottom', alpha=0.7)

# **Set logarithmic scale for population axis**
plt.xscale('log')  

# Add labels and title
plt.title('Relationship Between Proportion of Global and Population (Log Scale)', fontsize=14)
plt.xlabel('Population (2023) - Log Scale', fontsize=12)
plt.ylabel('Proportion of Global', fontsize=12)
#plt.grid(True, linestyle='--', alpha=0.6, which='both')  # Apply grid to both major and minor ticks

# Show the plot
plt.tight_layout()
plt.show()
