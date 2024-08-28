import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import os

csv_path = './headline_data/'

# Function to replace double quotes with single quotes for consistent comparison and readability
def escape_quotes(text):
    return text.replace('"', "'")

# Function to load and classify headlines
def classify_headlines():
    # Load the CSV file containing the headlines and URLs
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
    headlines_list = (headlines_df['Headline'] + ' ' + headlines_df['Description']).astype(str).tolist()

    # Classify each headline individually and collect the results
    results = sentiment_pipeline(headlines_list, truncation=True, max_length=128)

    # Add the results to the DataFrame
    headlines_df['label'] = [result['label'] for result in results]
    headlines_df['score'] = [result['score'] for result in results]

    # Filter for positive sentiments and sort by confidence
    positive_headlines = headlines_df[headlines_df['label'] == 'POS'].sort_values(by='score', ascending=False)

    # Calculate the positivity score
    positive_count = headlines_df[headlines_df['label'] == 'POS'].shape[0]
    non_positive_count = headlines_df[headlines_df['label'] != 'POS'].shape[0]

    if non_positive_count == 0:
        print("No negative or neutral headlines available for comparison.")
    else:
        positivity_score = positive_count / non_positive_count
        print(f"Positivity Score: {positivity_score:.2f}")

    # Domain count limit
    domain_count = {}

    new_top_4_positive_headlines = []
    for _, row in positive_headlines.iterrows():
        clean_headline = escape_quotes(row['Headline'])
        domain = row['Domain']

        if domain not in domain_count:
            domain_count[domain] = 0

        if domain_count[domain] < 1:
            if clean_headline not in existing_headlines:
                new_top_4_positive_headlines.append(row)
                existing_headlines.add(clean_headline)
                domain_count[domain] += 1

            if len(new_top_4_positive_headlines) == 4:
                break

    with open(used_headlines_file, 'a', encoding='utf-8', newline='') as file:
        for row in new_top_4_positive_headlines:
            file.write(f"\"{escape_quotes(row['Headline'])}\",\"{row['URL']}\",\"{escape_quotes(row['Description'])}\",\"{escape_quotes(row['Domain'])}\",\"{positivity_score:.2f}\"\n")

    print(f"New Top 4 Positive Headlines: {[row['Headline'] for row in new_top_4_positive_headlines]}")


# Existing headlines and used headlines file check
used_headlines_file = csv_path + 'used_headlines.csv'
if os.path.exists(used_headlines_file):
    used_headlines_df = pd.read_csv(used_headlines_file, encoding='utf-8')
    existing_headlines = set(used_headlines_df['Headline'].apply(escape_quotes))
else:
    existing_headlines = set()
    pd.DataFrame(columns=['Headline', 'URL', 'Description', 'Domain', 'Score']).to_csv(used_headlines_file, index=False, encoding='utf-8')


classify_headlines()
