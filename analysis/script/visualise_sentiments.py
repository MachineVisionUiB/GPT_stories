
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

make_scatterplot()