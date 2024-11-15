import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2, venn3
import os

# Load the data

directory = '/Users/hermannwigers/Documents/AI STORIES/GPT_stories/data/stories/full_stories_analysis/word_freq'
# List all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]


# Load each file into a DataFrame
dfs = [pd.read_csv(os.path.join(directory, file)).set_index("Word") for file in csv_files]

# Create a list of keys (file names without extensions)
keys = [os.path.splitext(file)[0] for file in csv_files]

# Merge the data into one DataFrame with keys
merged_df = pd.concat(dfs, axis=1, keys=keys).fillna(0)
merged_df.columns = merged_df.columns.droplevel(1)  # Simplify column names

# Display merged DataFrame
print(merged_df)

# Jaccard Similarity
word_sets = [set(df.index) for df in dfs]
jaccard_index = len(set.intersection(*word_sets)) / len(set.union(*word_sets))
print(f"Jaccard Similarity: {jaccard_index:.2f}")

# Cosine Similarity
cosine_sim = cosine_similarity(merged_df.T)

# Custom tick labels (e.g., shorter or more descriptive names)
custom_labels = [name[10:] if len(name) > 10 else name for name in keys]
sns.heatmap(cosine_sim, annot=True, xticklabels=custom_labels, yticklabels=custom_labels, cmap="coolwarm")
plt.title("Cosine Similarity Heatmap")
plt.tight_layout()
plt.savefig('stories_cosine_similarity_heatmap.png')
plt.show()

# # Venn Diagram (limited to 2 or 3 files)
# if len(word_sets) == 2:
#     venn2(word_sets, keys[:2])
# elif len(word_sets) == 3:
#     venn3(word_sets, keys[:3])
# else:
#     print("Venn diagrams only support up to 3 sets.")
# plt.title("Word Overlap")
# plt.show()
