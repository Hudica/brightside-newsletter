import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import os

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

# File to store used headlines
used_headlines_file = 'used_headlines.csv'

# Ensure the used_headlines.csv file exists
if not os.path.exists(used_headlines_file):
    pd.DataFrame(columns=['Headline', 'URL']).to_csv(used_headlines_file, index=False)

# Read existing headlines from the used_headlines.csv file
used_headlines_df = pd.read_csv(used_headlines_file)
existing_headlines = set(used_headlines_df['Headline'].tolist())

# Initialize a list to hold the top 3 new positive headlines
new_top_3_positive_headlines = []

# Iterate through the positive headlines to find the top 3 new ones
for index, row in positive_headlines.iterrows():
    if row['Headline'] not in existing_headlines:
        new_top_3_positive_headlines.append(row)
        if len(new_top_3_positive_headlines) == 3:
            break

# Add new headlines to the used_headlines.csv file
with open(used_headlines_file, 'a') as file:
    for row in new_top_3_positive_headlines:
        file.write(f"{row['Headline']},{row['URL']}\n")
        print(f"Added headline -> {row['Headline']}")
        print(f"{row['Headline']}, {row['URL']} -> {row['label']} {row['score']}")

# Print the final new headlines
print(f"New Top 3 Positive Headlines: {new_top_3_positive_headlines}")
