from transformers import pipeline
from transformers import AutoTokenizer

# Load the model and tokenizer into a sentiment analysis pipeline
sentiment_pipeline = pipeline("text-classification", model='./saved_model', tokenizer='./saved_model')
tokenizer = AutoTokenizer.from_pretrained('finiteautomata/bertweet-base-sentiment-analysis')

# Example of testing the model
texts = [
    "CNN commentator blasts Kamala Harris for working to ‘erase all evidence’ she was border czar",
    "Jordan Chiles Makes The Coolest Gesture Of The Night In U.S. Gymnastics Team Win",
    "Historian who correctly predicted almost every US election since 1984 gives Harris vs Trump verdict",
    "Boxing controversy rocks the Olympic Games as Australian star is 'robbed' of victory over reigning world champion: 'I won that fight'",
    "Paper cut physics pinpoints the most hazardous types of paper",
    "Teen girl’s joy at getting a rare party invite goes viral: ‘We all want to feel like we belong’",
    "A boy was in tears because he didn't have PJs for Pajamas Day. His bus driver came to the rescue",
    "Dutch water innovation: Turning sewage into safe drinking water offers hope amidst global droughts"
]

results = [sentiment_pipeline(text) for text in texts]
for text, result in zip(texts, results):
    print(f"Text: {text}\nPredicted Sentiment: {result[0]['label']} - Score: {result[0]['score']:.4f}\n")