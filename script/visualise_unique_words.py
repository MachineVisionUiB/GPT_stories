import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Jill's still messy code for exploring the unique words dataset by adding more variables like population, region etc
# This is a work in progress and will be cleaned up later

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

# Ensure population and frequency contain only finite values
data = data.replace([float('inf'), float('-inf')], pd.NA)  # Convert infinite values to NaN
data = data.dropna(subset=['population', 'frequency'])  # Remove NaN values

# All the countries where word frequency is greater than 1000 have stop words 
# in the local language as most unique word, so filter them out.


# Assign each region a unique color
region_colors = {region: idx for idx, region in enumerate(data['region'].unique())}
data['region_color'] = data['region'].map(region_colors)


print(data.head())
print(data.columns)

# Save the data to a CSV file
#data.to_csv('data/unique_words_by_country_expanded.csv', index=False)

# Display the merged data
print("Data loaded, will now visualise the data")

# -------------------Testing  Visualisations ------------------- 

# ----- Wordclouds by region sized by inverse of proportion -----

# Define the regions
regions = data['region'].unique()

# Loop through each region to create a word cloud
for region in regions:
    # Filter data for the region
    subset = data[data['region'] == region]
    
    # Create a dictionary of words and their inverse proportions
    word_weights = {row['word']: 1 / row['proportion_of_global'] for _, row in subset.iterrows()}
    # (using inverse because otherwise the words that are ONLY
    # used in that country are biggest, and those words are usually
    # stop words or place names that we should really weed out of dataset)=

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_weights)
    
    # Plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Most unique words for {region}", fontsize=24)
    plt.suptitle("Bigger words are used in more different countries", fontsize=10)
    
    #save the wordclouds
    plt.savefig(f'images/wordcloud_inverse_uniqueness_{region}.png')



# ---- Use FacetGrid in Seaborn to create a grid of scatter plots ----


""" # Set up FacetGrid
g = sns.FacetGrid(data, col="region", col_wrap=3, sharex=True, sharey=True, height=4)

# Map scatter plot onto each facet
g.map_dataframe(
    sns.scatterplot,
    x="population",
    y="proportion_of_global",
    alpha=0.7,
    edgecolor="k"
)

# Add labels manually for each point
for ax, region in zip(g.axes.flat, data['region'].unique()):
    subset = data[data["region"] == region]
    for i, row in subset.iterrows():
        label = f"{row['name']} ({row['word']})"
        ax.text(
            row['population'], 
            row['proportion_of_global'], 
            label, 
            fontsize=6, 
            ha='right', 
            va='bottom', 
            alpha=0.7
        )

# Apply log scale to population
for ax in g.axes.flat:
    ax.set_xscale("log")
    ax.set_yscale("log")  

# Set titles and labels
g.set_titles(col_template="{col_name}")
g.set_axis_labels("Population (Log Scale)", "Proportion of Global")

# Show the plots
plt.show()


exit() """



""" plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    data['population'],
    data['frequency'],
    c=data['region_color'],  # Use region-based colors
    cmap='tab10',  # Choose a colormap (tab10 has distinct colors)
    alpha=0.7,
    edgecolors='k'
)

# Add a legend for the regions
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plt.cm.tab10(region_colors[r] / 10), markersize=10)
           for r in region_colors]
plt.legend(handles, region_colors.keys(), title="Regions", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.title('Relationship Between Population and Frequency by Region', fontsize=14)
plt.xlabel('Population (Log Scale)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Set logarithmic scale for population axis
plt.xscale('log')

# Add labels for each point
for i, row in data.iterrows():
    label = f"{row['name']} ({row['word']})"
    plt.text(row['population'], row['frequency'], label, fontsize=8, ha='right', va='bottom', alpha=0.7)

plt.tight_layout()
plt.show()

exit() """


# ------------------- Visualisation -------------------


# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(
    data['population'], 
    data['proportion_of_global'], 
    c=data['region_color'],  # Use region-based colors
    cmap='tab10',  # Choose a colormap (tab10 has distinct colors)
    alpha=0.7, 
    edgecolors='k')

# Add a legend for the regions
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=plt.cm.tab10(region_colors[r] / 10), markersize=10)
           for r in region_colors]
plt.legend(handles, region_colors.keys(), title="Regions", bbox_to_anchor=(1.05, 1), loc='upper left')

# Add labels for each point
for i, row in data.iterrows():
    label = f"{row['name']} ({row['word']})"
    plt.text(row['population'], row['proportion_of_global'], label, fontsize=8, ha='right', va='bottom', alpha=0.7)

# **Set logarithmic scale for population axis**
plt.xscale('log')  

# Add labels and title
plt.title('No correlation population size - words unique to country (Log Scale)', fontsize=14)
plt.xlabel('Population (2023) - Log Scale', fontsize=12)
plt.ylabel('Higher means word not used by other countries', fontsize=12)
#plt.grid(True, linestyle='--', alpha=0.6, which='both')  # Apply grid to both major and minor ticks

plt.savefig('images/scatterplot_uniqueness_population.png')
