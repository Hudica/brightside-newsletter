from transformers import pipeline
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Load the sentiment analysis pipeline with your saved model
sentiment_pipeline = pipeline("text-classification", model='./saved_model', tokenizer='./saved_model')

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
("City Parking Regulations Updated", 1),
("Revolutionary Battery Extends Electric Cars' Range", 2),
("Legal Reforms Set to Enhance Worker Rights", 2),
("Community Celebrates the Opening of a New Local Library", 2),
("Breakthrough Study Doubles Survival Rates for Rare Disease", 2),
("City's New Recycling Program Cuts Waste by 30%", 2),
("Innovative App Connects Leftover Food with Homeless Shelters", 2),
("Local Jazz Band Wins International Music Competition", 2),
("Nonprofit Achieves Goal of Planting One Million Trees", 2),
("New Green Space Initiative Aims to Revitalize Downtown", 2),
("Scientist Wins Award for Lifetime Contributions to Physics", 2),

("Study Finds No Significant Impact from Latest Education Policy", 1),
("Local Council Delays Decision on New Building Development", 1),
("Conference on Sustainable Agriculture Draws Global Experts", 1),
("Weekly Market Summary: Stocks Hold Steady Amidst Volatility", 1),
("City Announces Minor Adjustments to Public Transport Schedules", 1),
("New Study Shows Steady Trends in Consumer Confidence", 1),
("Experts Discuss Cybersecurity at Annual Tech Conference", 1),
("Regional Weather Forecast Predicts Mild Winter", 1),
("Historical Society Holds Annual Meet to Discuss Preservation Techniques", 1),

("Government Faces Backlash Over New Internet Regulation Bill", 0),
("Investigation Uncovers Corruption at Local Town Hall", 0),
("Factory Pollution Exceeds Legal Limits, Sparks Health Concerns", 0),
("Major Company Recalls Faulty Appliances Amid Safety Fears", 0),
("Protests Erupt Following Verdict in High-Profile Case", 0),
("Wildfire Destroys Hundreds of Homes in Coastal Area", 0),
("Data Breach at Large Corporation Compromises User Privacy", 0),
("Diplomatic Talks Break Down Over Trade Disagreements", 0),
("Economic Downturn Results in Record High Unemployment", 0),
("City Struggles to Manage Overcrowded Public Transport System", 0),

("New Therapy Found Effective Against Childhood Leukemia", 2),
("Local Startup's Innovation Reduces Energy Costs for Schools", 2),
("Artist's Mural Celebrates Diversity and Unity", 2),
("Upcoming Workshop Aims to Boost Small Business Success", 2),
("Research Grants Increase for Renewable Energy Projects", 2),
("Community Health Clinic Expands to Serve More Residents", 2),
("Annual Film Festival Features Record Number of Female Directors", 2),
("Technology for Clean Water Wins Environmental Award", 2),
("Veteran's New Book Details Journey of Recovery and Hope", 2),
("Global Initiative to End Hunger Receives Significant Funding", 2),

("Public Debate on New Environmental Bill Lacks Clear Consensus", 1),
("City Report Details Progress in Reducing Street Congestion", 1),
("New Guidelines Issued for Safer School Environments", 1),
("Local University to Host Panel on Future of Digital Education", 1),
("Telecom Companies to Update Infrastructure for Improved Service", 1),
("Annual Health Report Shows Stable Disease Rates", 1),
("Tech Companies to Enhance Security Measures", 1),
("Cultural Festival Adjusts to New Format to Maintain Traditions", 1),
("Experts Call for More Research on Climate Adaptation Measures", 1),
("Trade Show Highlights New Trends in Consumer Electronics", 1)


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
