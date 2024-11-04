import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('stopwords')


# Load dataset
df = pd.read_csv('/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/countries_samples/american_stories.csv')
texts = df['Story'].tolist()

# Preprocessing function
def preprocess(text):
    # Tokenize, remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return ' '.join(tokens)

# Apply preprocessing
processed_texts = [preprocess(text) for text in texts]

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_texts)

# Apply LSA (Truncated SVD)
num_topics = 5
lsa_model = TruncatedSVD(n_components=num_topics, random_state=42)
lsa_topic_matrix = lsa_model.fit_transform(X)

# Get the top words for each topic
def get_top_words(model, vectorizer, n_words=10):
    words = vectorizer.get_feature_names_out()
    top_words = []
    for topic in model.components_:
        top_indices = topic.argsort()[-n_words:][::-1]
        top_words.append([words[i] for i in top_indices])
    return top_words

top_words = get_top_words(lsa_model, vectorizer)
for i, words in enumerate(top_words):
    print(f"Topic {i}: {', '.join(words)}")

# Plot the topics
def plot_lsa_topics(lsa_topic_matrix, num_topics):
    plt.figure(figsize=(10, 7))
    for topic_num in range(num_topics):
        plt.scatter(lsa_topic_matrix[:, topic_num], np.zeros(lsa_topic_matrix.shape[0]), label=f"Topic {topic_num}")
    
    plt.xlabel("Topic Dimension")
    plt.ylabel("Frequency")
    plt.legend()
    plt.title("LSA Topics")
    plt.show()

plot_lsa_topics(lsa_topic_matrix, num_topics)