from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import pandas as pd

# Load the CSV file containing the headlines and URLs
csv_file = 'headlines.csv'
headlines_df = pd.read_csv(csv_file)

# Ensure the column names are correct (case-sensitive)
headlines_df.columns = [col.strip() for col in headlines_df.columns]

# Load the tokenizer and model from the saved directory
model_path = './saved_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Initialize the pipeline
sentiment_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Ensure the headlines are in the correct format (list of strings)
headlines_list = headlines_df['Headline'].astype(str).tolist()

# Classify each headline individually and collect the results
results = [sentiment_pipeline(headline)[0] for headline in headlines_list]

# Add the results to the DataFrame
headlines_df['label'] = [result['label'] for result in results]
headlines_df['score'] = [result['score'] for result in results]

# Filter for positive sentiments and sort by confidence
positive_headlines = headlines_df[headlines_df['label'] == 'POS'].sort_values(by='score', ascending=False)

# Select top 3 headlines
top_3_positive_headlines = positive_headlines.head(3)

# Print the top 3 positive headlines with their URLs
for index, row in top_3_positive_headlines.iterrows():
    print(f"{row['Headline']}, {row['Website']} -> {row['label']} {row['score']}")
