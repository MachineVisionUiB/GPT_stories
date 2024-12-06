import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the CSV file
filename = input("Enter the file name: ")+"_sentiment.csv"
df = pd.read_csv('/Users/hermannwigers/Documents/AI STORIES/GPT_stories/samples/sentiment/'+filename)

# Plot the distribution of Polarity and Subjectivity
plt.figure(figsize=(14, 6))

# Plot for Polarity
plt.subplot(1, 2, 1)
sns.histplot(df['Polarity'].dropna(), kde=True)
plt.title('Distribution of Polarity')
plt.xlabel('Polarity')
plt.ylabel('Frequency')

# Plot for Subjectivity
plt.subplot(1, 2, 2)
sns.histplot(df['Subjectivity'].dropna(), kde=True)
plt.title('Distribution of Subjectivity')
plt.xlabel('Subjectivity')
plt.ylabel('Frequency')

# Set the title for the whole figure
plt.suptitle(filename, fontsize=16)

plt.tight_layout()
plt.show()

# Perform normality tests
def perform_normality_tests(column):
    k2, p = stats.normaltest(column.dropna())
    print(f'Normality test p-value for {column.name}: {p}')
    if p < 0.05:
        print(f'{column.name} is likely not normally distributed.')
    else:
        print(f'{column.name} is likely normally distributed.')

# Apply the normality tests
perform_normality_tests(df['Polarity'])
perform_normality_tests(df['Subjectivity'])
