import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# Load dataset
df = pd.read_csv('plot_summaries.csv')
summaries = df['summary'].tolist()