from transformers import pipeline

# Use a Norwegian model from Hugging Face
classifier = pipeline("sentiment-analysis", model="NbAiLab/nb-bert-base-ncc-sentiment")

# Sample Norwegian text
text = "Jeg elsker dette produktet! Det er fantastisk."

# Perform sentiment analysis
result = classifier(text)

# Display the result
print(result)