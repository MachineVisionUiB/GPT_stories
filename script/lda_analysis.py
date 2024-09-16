import pandas as pd
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import warnings
import webbrowser


warnings.filterwarnings("ignore", category=DeprecationWarning, module='joblib.externals.loky.backend.fork_exec')




# Bypass SSL certificate verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Load dataset
df = pd.read_csv('/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/1000_jpn_stories.csv')
summaries = df['Story'].tolist()

# Preprocessing
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
    return tokens

processed_summaries = [preprocess(summary) for summary in summaries]

# Create dictionary and corpus
dictionary = corpora.Dictionary(processed_summaries)
corpus = [dictionary.doc2bow(summary) for summary in processed_summaries]

# Train LDA model
num_topics = 10
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10, random_state=42)

# Display topics
topics = lda_model.print_topics(num_topics=num_topics, num_words=5)
for topic in topics:
    print(topic)

lda_vis = gensimvis.prepare(lda_model, corpus, dictionary)
# Save the visualization as an HTML file
pyLDAvis.save_html(lda_vis, 'jpn1000_lda_visualization_t10.html')

# Open the HTML file in the default web browser
webbrowser.open('jpn1000_lda_visualization_t10.html')