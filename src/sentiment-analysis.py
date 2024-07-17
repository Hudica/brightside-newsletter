from transformers import pipeline

def main():
    # Load the sentiment analysis pipeline
    model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    model_revision = "main"  

    classifier = pipeline("sentiment-analysis", model=model_name, revision=model_revision)

    # Example texts
    texts = [
    "Global Protests Demand Action on Climate Change Amidst Economic Concerns",
    "Celebrated Author Releases Book Highlighting the Joys of Sustainable Living",
    "Local Startup Aims to Revolutionize Recycling, Faces Regulatory Hurdles",
    "Community Rejoices as New Park Opens, But Traffic Congestion Worsens",
    "Scientists Discover Promising Cure for Rare Disease, Yet Funding Remains Uncertain",
    "Renewable Energy Investments Hit Record High Despite Political Pushback",
    "Wildlife Conservation Efforts Show Hopeful Progress in Tiger Populations",
    "Economic Downturn Leads to Increased Community Gardening Initiatives",
    "Tech Giant Faces Backlash Over Data Privacy Concerns Despite Charitable Contributions",
    "Diplomatic Talks Show Promise, Yet Concerns Over Arms Buildup Remain",
    "Innovative Water Purification Technique Developed, Faces Big Oil Opposition",
    "Artificial Intelligence Helps Improve Diagnosis Accuracy, Raises Ethical Questions",
    "Historic Theater Restoration Completed with Overwhelming Community Support, Faces Long-Term Sustainability Questions",
    "Breakthrough in Alzheimer’s Research Offers Hope, Concerns About Access to Treatment Arise",
    "International Literacy Program Expands Rapidly, Critics Question Curriculum Choices",
    "Major City Implements Green Roof Policy, Struggles with Maintenance Costs",
    "Famed Wildlife Photographer Captures Endangered Species, Raises Awareness About Habitat Destruction",
    "New Documentary on Coral Reefs Receives Praise for Awareness, Criticism for Lack of Depth in Solutions",
    "Veterans to Receive Increased Benefits, Controversy Over Funding Sources Ensues",
    "Beach Cleanup Event Draws Thousands, Highlights Ongoing Pollution Challenges"
]



    # Perform sentiment analysis
    results = classifier(texts)

    # Print the results
    for text, result in zip(texts, results):
        print(f"Text: {text}")
        print(f"Sentiment: {result['label']}, Confidence: {result['score']:.2f}")
        print("")

if __name__ == "__main__":
    main()
