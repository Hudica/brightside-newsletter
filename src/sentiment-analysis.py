from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoTokenizer
from datasets import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split

#First we want to read in the training data
data_path = 'data/data.csv'
data = pd.read_csv(data_path)

# Convert the DataFrame into a Hugging Face dataset
dataset = Dataset.from_pandas(data)

#Bring in the model
model_name = "finiteautomata/bertweet-base-sentiment-analysis"

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Function to tokenize the data
def tokenize_function(examples):
    return tokenizer(examples['headline'], truncation=True, padding="max_length", max_length=128)

# Apply tokenization to the dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Splitting the dataset
train_dataset, eval_dataset = train_test_split(tokenized_datasets, test_size=0.1)

#Model/Trainer setup
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    logging_dir='./logs',
)

model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)


#Creating a trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,  
    eval_dataset=eval_dataset,    
    tokenizer=tokenizer
)

trainer.train()
