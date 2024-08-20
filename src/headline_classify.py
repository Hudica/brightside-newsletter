import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import os

csv_path = './headline_data/'

# Function to replace double quotes with single quotes for consistent comparison and readability
def escape_quotes(text):
    return text.replace('"', "'")

# Function to load and classify headlines
def classify_headlines():
    # Load the CSV file containing the headlines and URLss
    csv_file = csv_path + 'headlines.csv'
    headlines_df = pd.read_csv(csv_file, encoding='utf-8')

    # Ensure the column names are correct (case-sensitive)
    headlines_df.columns = [col.strip() for col in headlines_df.columns]

    # Load the tokenizer and model from the saved directory
    model_path = './saved_model'
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    # Initialize the pipeline
    sentiment_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # Ensure the headlines are in the correct format (list of strings)
    headlines_list = headlines_df['Headline'] + ' ' + headlines_df['Description'].astype(str).tolist()

    # Classify each headline individually and collect the results
    results = [sentiment_pipeline(headline)[0] for headline in headlines_list]

    # Add the results to the DataFrame
    headlines_df['label'] = [result['label'] for result in results]
    headlines_df['score'] = [result['score'] for result in results]

    # Filter for positive sentiments and sort by confidence
    positive_headlines = headlines_df[headlines_df['label'] == 'POS'].sort_values(by='score', ascending=False)

    # File to store used headlines
    used_headlines_file = csv_path + 'used_headlines.csv'

    # Read existing headlines from the used_headlines.csv file
    if os.path.exists(used_headlines_file):
        used_headlines_df = pd.read_csv(used_headlines_file, encoding='utf-8')
        existing_headlines = set(used_headlines_df['Headline'].apply(escape_quotes))
    else:
        existing_headlines = set()
        pd.DataFrame(columns=['Headline', 'URL', 'Description']).to_csv(used_headlines_file, index=False, encoding='utf-8')

    new_top_4_positive_headlines = []

    # Iterate through the positive headlines to find the top 4 new ones
    for _, row in positive_headlines.iterrows():
        clean_headline = escape_quotes(row['Headline'])
        if clean_headline not in existing_headlines:
            new_top_4_positive_headlines.append(row)
            existing_headlines.add(clean_headline)
            if len(new_top_4_positive_headlines) == 4:
                break

    with open(used_headlines_file, 'a', encoding='utf-8', newline='') as file:
        for row in new_top_4_positive_headlines:
            file.write(f"\"{escape_quotes(row['Headline'])}\",\"{row['URL']}\",\"{escape_quotes(row['Description'])}\",\"{escape_quotes(row['Domain'])}\"\n")

    print(f"New Top 4 Positive Headlines: {[row['Headline'] for row in new_top_4_positive_headlines]}")

classify_headlines()
