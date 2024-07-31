from transformers import pipeline
from transformers import AutoTokenizer

# Load the model and tokenizer into a sentiment analysis pipeline
sentiment_pipeline = pipeline("text-classification", model='./saved_model', tokenizer='./saved_model')
tokenizer = AutoTokenizer.from_pretrained('finiteautomata/bertweet-base-sentiment-analysis')

# Example of testing the model
texts = [
    "Trump faces backlash over comments on military strategy",
    "Public library launches summer reading program",
    "Daredevil Grandma to test new roller coaster ride"
]

results = [sentiment_pipeline(text) for text in texts]
for text, result in zip(texts, results):
    print(f"Text: {text}\nPredicted Sentiment: {result[0]['label']} - Score: {result[0]['score']:.4f}\n")