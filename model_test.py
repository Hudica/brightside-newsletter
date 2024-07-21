from transformers import pipeline

# Load the model and tokenizer into a sentiment analysis pipeline
sentiment_pipeline = pipeline("text-classification", model='./saved_model', tokenizer='./saved_model')

# Example of testing the model
texts = [
    "Thousands of flights in US grounded by massive outage",
    "Father of Trump gunman called police about son before attack",
    "US journalist Gershkovich jailed on espionage charges",
    "Is cold water swimming good for you?",
    "The strange maths at work in the Tour de France",
    "Can this mineral help reduce anxiety?",
    "Daredevil grandma to test new rollercoaster rides",
    "Britain's most stunning bohemian gardens",
    "Where to get the best pizza in Chicago"
]

results = [sentiment_pipeline(text) for text in texts]
for text, result in zip(texts, results):
    print(f"Text: {text}\nPredicted Sentiment: {result[0]['label']} - Score: {result[0]['score']:.4f}\n")