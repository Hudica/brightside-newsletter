from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd

#First we want to read in the training data
data_path = 'data/data.csv'
data = pd.read_csv(data_path)

# Convert the DataFrame into a Hugging Face dataset
dataset = Dataset.from_pandas(data)

#Bring in the model
model_name = "finiteautomata/bertweet-base-sentiment-analysis"
   