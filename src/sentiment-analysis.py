from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoTokenizer
from datasets import Dataset
import pandas as pd

# Read the training data
data_path = 'data/data.csv'
data = pd.read_csv(data_path)

# Convert the DataFrame into a Hugging Face dataset
dataset = Dataset.from_pandas(data)

# Load the tokenizer and model
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# Function to tokenize the data
def tokenize_function(examples):
    return tokenizer(examples['headline'], truncation=True, padding="max_length", max_length=64)

# Apply tokenization to the dataset
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Split the dataset into training and validation sets
split_datasets = tokenized_datasets.train_test_split(test_size=0.1)
train_dataset = split_datasets['train']
eval_dataset = split_datasets['test']

# Model/Trainer setup
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    logging_dir='./logs',
    learning_rate=2e-04,
    lr_scheduler_type='linear',  
    eval_strategy="epoch"
)

# Create a trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained('./saved_model')
tokenizer.save_pretrained('./saved_model')
