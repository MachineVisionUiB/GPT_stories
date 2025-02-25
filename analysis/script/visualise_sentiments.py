
from matplotlib import pyplot as plt
import pandas as pd

def make_boxplot():

    df = pd.read_csv("analysis/data/all_countries_sentiments.csv")

    #make box plot where x is the sentiment and y is the confidence

    # Create a box plot of the sentiment confidence scores
    df.boxplot(column='confidence', by='sentiment', grid=False)
    plt.title("Sentiment Confidence Scores by Sentiment")
    plt.suptitle("")
    plt.ylabel("Confidence Score")
    plt.xlabel("Sentiment")
    plt.show()

def make_scatterplot():
    
    df = pd.read_csv("analysis/data/all_countries_sentiments.csv")

    #make scatter plot where x is the sentiment and y is the confidence

    # Create a scatter plot of the sentiment confidence scores
    df.plot.scatter(x='sentiment', y='population')
    plt.title("Sentiment  by population")
    plt.ylabel("Population")
    plt.xlabel("Sentiment")
    plt.show()



def make_proportional_stacked_barchart(df, group_by="country", region=None, country_list=None):
    """
    Creates a proportional stacked bar chart of sentiment distribution.
    
    Parameters:
    - df (pd.DataFrame): The dataset containing sentiment data.
    - group_by (str): Aggregation level, "country" or "region".
    - region (str, optional): If specified, filters data to this specific region.
    - country_list (list, optional): If specified, filters data to these specific countries.
    
    Returns:
    - A stacked bar chart showing proportional sentiment distribution.
    """

    # Define fixed colours for each sentiment
    sentiment_colours = {
        "sadness": "blue",
        "love": "red",
        "anger": "brown",
        "joy": "green",
        "surprise": "purple",
        "fear": "orange"
        }
    
    # Apply filters
    if region:
        df = df[df["region"] == region]
    
    if country_list:
        df = df[df["country_name"].isin(country_list)]
    
    # Determine grouping level
    if group_by == "region":
        group_col = "region"
    elif group_by == "country":
        group_col = "country_name"
    else:
        raise ValueError("Invalid group_by value. Valid values are 'region' or 'country'.")
    
    # Aggregate sentiment counts
    sentiment_counts = df.groupby([group_col, "sentiment"]).size().unstack().fillna(0)
    print(sentiment_counts)
    
    # Convert to proportions
    sentiment_proportions = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0)

    # Ensure the colours are applied in the correct order
    available_sentiments = sentiment_proportions.columns.tolist()
    colours = [sentiment_colours[sent] for sent in available_sentiments if sent in sentiment_colours]


    # Plot
    plt.figure(figsize=(14, 7))
    sentiment_proportions.plot(kind="bar", 
                               stacked=True, 
                               figsize=(14, 7),
                               color=sentiment_colours)

    # Title and labels
    title = "Proportional Sentiment Distribution"
    if region:
        title += f" in {region}"
    if country_list:
        title += f" for Selected Countries"
    
    plt.title(title)
    plt.ylabel("Proportion of Sentiments")
    plt.xlabel(group_col.replace("_", " ").title())
    plt.xticks(rotation=90)
    plt.legend(title="Sentiment", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()



# Example Usage:
df = pd.read_csv("analysis/data/all_countries_sentiments.csv")
# make_proportional_stacked_barchart(df, group_by="country", region="Europe")
# make_proportional_stacked_barchart(df, group_by="region")
# make_proportional_stacked_barchart(df, group_by="country", country_list=["Norway", "Sweden", "Denmark", "Finland", "Australia", "USA", "Canada", "United Kingdom", "Ukraine", "Russia", "Palestine", "Israel"])
make_proportional_stacked_barchart(df, group_by="country", country_list=["Palestine", "Israel"])



# make_scatterplot()

