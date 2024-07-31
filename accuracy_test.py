from transformers import pipeline
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Load the sentiment analysis pipeline with your saved model
sentiment_pipeline = pipeline("text-classification", model='./saved_model', tokenizer='./saved_model')

# List of example headlines for sentiment analysis with corresponding labels
headlines = [
    # Positive Headlines
("Major Tech Firm Announces Breakthrough in Renewable Energy", 2),
("Community Celebrates Opening of New Local Library", 2),
("Local Athlete Wins Gold at International Track Event", 2),
("Innovative Startup Reduces Plastic Waste with New Biodegradable Material", 2),
("Charity Event Raises Record Funds for Childhood Cancer Research", 2),
("Veterans Honored with New Monument in Downtown Park", 2),
("Popular Music Festival Returns with Exciting Lineup", 2),
("Film on Wildlife Conservation Wins Prestigious International Award", 2),
("City's New Recycling Initiative Cuts Waste by 30%", 2),
("High School Robotics Team Wins National Competition", 2),
("Pet Adoption Rates Reach All-Time High", 2),
("Historic Downtown Area Restored and Reopened to Public", 2),
("New Art Exhibit Features Works from Local Immigrant Artists", 2),
("Young Inventor Creates Device to Clean Oceans", 2),
("Endangered Species Numbers on the Rise Thanks to Conservation Efforts", 2),
("Local Unemployment Rates Drop to Record Low", 2),
("Major Corporation to Invest $1 Billion in Clean Energy", 2),
("Breakthrough in Alzheimer's Treatment Shows Promise in Early Trials", 2),
("International Culinary Festival Spotlights Vegan Cuisine", 2),
("Nation Marks 10 Years of Peace with Cultural Festival", 2),
("Massive Wildfire Destroys Hundreds of Homes", 0),
("Corruption Probe Indicts High-Profile Politicians", 0),
("Global Stock Market Crash Leads to Economic Panic", 0),
("Cyber Attack Compromises National Security Agency", 0),
("Severe Flooding Displaces Thousands of Residents", 0),
("Bridge Collapse During Rush Hour Causes Fatalities", 0),
("Air Quality Deteriorates to Hazardous Levels in Major Cities", 0),
("Health Department Recalls Contaminated Meat Nationwide", 0),
("Bankruptcy of Major Airline Strands Thousands", 0),
("Drug Trafficking Operation Busted, Dozens Arrested", 0),
("Local Factory Pollution Causes Respiratory Illnesses", 0),
("Historic Strike Disrupts National Rail Services", 0),
("Major Oil Spill Threatens Wildlife Reserve", 0),
("Violent Protests Erupt Over Government Policy", 0),
("Controversial Political Figure Acquitted in High-Profile Trial", 0),
("Increase in College Tuition Fees Sparks Student Protests", 0),
("Flooded Rivers Contaminate Drinking Water Supply", 0),
("Housing Market Crash Leaves Many Homeless", 0),
("Outbreak of Food Poisoning at Popular Restaurant", 0),
("Pharmaceutical Giant Fined for Illegal Practices", 0),
("Subway System Shutdown Due to Safety Concerns", 1),
("Annual Budget Report Released by Local Government", 1),
("City Council Votes on New Public Transport Policy", 1),
("Museum Attendance Remains Steady", 1),
("Routine Road Maintenance Scheduled for Next Month", 1),
("Local College Announces Updated Admissions Policy", 1),
("New Study Reveals Trends in Consumer Electronics Usage", 1),
("Researchers Publish Findings on Recent Meteorological Changes", 1),
("Weekly Guide to TV Listings", 1),
("City Parking Regulations Updated", 1)


]

# Extract headlines and labels
headlines_text = [headline[0] for headline in headlines]
manual_labels = [headline[1] for headline in headlines]

# Predict sentiments using the model
predicted_labels = [sentiment_pipeline(text)[0]['label'] for text in headlines_text]

# Map string labels from the model to numeric labels
label_mapping = {'NEG': 0, 'POS': 2, 'NEU': 1}
predicted_labels_numeric = [label_mapping[label] for label in predicted_labels]

# Calculate accuracy
accuracy = accuracy_score(manual_labels, predicted_labels_numeric)
print(f"Model accuracy: {accuracy:.4f}")

# Generate and plot the confusion matrix
cm = confusion_matrix(manual_labels, predicted_labels_numeric, labels=[0, 1, 2])
plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['negative', 'positive', 'neutral'], yticklabels=['negative', 'positive', 'neutral'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Print the classification report
report = classification_report(manual_labels, predicted_labels_numeric, target_names=['NEG', 'positive', 'neutral'])
print(report)
