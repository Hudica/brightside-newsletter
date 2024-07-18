from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
import pandas as pd

#First we want to read in the training data
data_path = 'path_to_data_file'
data = pd.read_csv(data_path)

   