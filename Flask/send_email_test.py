from mailjet_rest import Client
import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables and set up Mailjet client
load_dotenv()
api_key = os.environ['MAILJET_API']
api_secret = os.environ['MAILJET_SECRET']
mailjet = Client(auth=(api_key, api_secret), version='v3')

csv_file_path = './headline_data/used_headlines.csv'
df = pd.read_csv(csv_file_path)
headlines = df['Headline'].tail(4).tolist()
urls = df['URL'].tail(4).tolist()
description = df['Description'].tail(4).tolist()
domains = df['Domain'].tail(4).tolist()

# Set up MongoDB connection
mongo_conn_string = os.getenv('MONGO_CONN_STRING')
client = MongoClient(mongo_conn_string)
db = client.BrightSideUsers
subscribers_collection = db.emails

def fetch_recipients():
    emails = [{'Email': doc['email']} for doc in subscribers_collection.find({}, {"_id": 0, "email": 1})]
    return emails
def generate_html_body(headlines, urls, description, domains):
    # HTML body of the email with creative and enhanced visual elements
    html_body = f"""
    <html>
    <body style="font-family: 'Helvetica', 'Arial', sans-serif; margin: 0; padding: 20px; text-align: center; background-color: #FFFFFF; color: #000000;">
        <h1 style="color: #DAA520; margin-bottom: 30px; font-size: 2.75em; border-bottom: 3px solid #DAA520;">The Brightside Newsletter</h1>

        <!-- Mission Statement Section -->
        <section style="padding: 20px; background-color: #FFFFFF; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); margin-bottom: 20px;">
            <h2 style="color: #333333; font-size: 1.5em; margin-bottom: 10px;"><u>Our Mission</u></h2>
            <p style="font-size: 1.2em; color: #333333;">In a world often overshadowed by negative news, my mission is to shine a light on the good. We scan the web for stories of hope, progress, and unity, bringing you a curated selection of positive news that inspires and uplifts. This newsletter is completely free and only exists to make people smile!</p>
        </section>

        <!-- How It Works Section -->
        <section style="padding: 20px; background-color: #F4F4F4; margin-bottom: 20px;">
            <h2 style="color: #333333; font-size: 1.5em; margin-bottom: 10px;"><u>How It Works</u></h2>
            <p style="font-size: 1.2em; color: #333333;">This newsletter uses a complex sentiment analysis model to identify the most positive and interesting headlines from established news outlets. This allows me to present you with news that not only informs but also contributes to a more optimistic worldview.</p>
        </section>

        <!-- Featured Headlines -->
        <section style="padding: 20px; background-color: #E8E8E8; margin-bottom: 20px;">
            <h2 style="color: #333333; font-size: 1.5em; border-bottom: 1px dashed #B8860B; margin-bottom: 20px;">Featured Headlines</h2>
    """
    for headline, url, desc, domain in zip(headlines, urls, description, domains):
        html_body += f"""
            <div style="background-color: #FFFFFF; padding: 15px; margin-bottom: 15px; border-left: 5px solid #DAA520; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
                <a href="{url}" target="_blank" style="color: #3366CC; text-decoration: none; font-size: 1.6em;"><strong>{headline}</strong></a>
                <p style="font-size: 1.2em; color: #444444; margin-top: 10px;">{desc}</p>
                <p style="font-size: 1em; color: #666666; margin-top: 5px;">(Credit: {domain})</p>
            </div>
        """
    html_body += f"""
        </section>

        <!-- Footer Section -->
        <footer style="padding: 20px; background-color: #D3D3D3; text-align: center; color: #696969; font-size: 0.9em; border-top: 1px solid #CCCCCC;">
            <p>Thank you for subscribing to The Brightside Newsletter. Stay tuned for more updates and positivity!</p>
            <p>Questions or feedback? Reach out <a href="mailto:brightside-news@hudica.info" style="color: #3366CC;">here</a>.</p>
            <p>Want to unsubscribe? <a href="https://news.hudica.info/unsubscribe" style="color: #3366CC; text-decoration: none;">Click here</a>.</p>
        </footer>
    </body>
    </html>
    """
    return html_body


def send_email(html_body, recipients):
    data = {
        'FromEmail': "brightside-news@hudica.info",
        'FromName': "Brightside Newsletter",
        'Recipients': singleRecipient,
        'Subject': "Brightside News Tuesday Edition!",
        'Text-part': "Your email flight plan!",
        'Html-part': html_body
    }
    result = mailjet.send.create(data=data)
    try:
        print("Status Code:", result.status_code)
        print("Response:", result.json())
    except ValueError:
        # Handling JSON decoding error
        print("Failed to decode JSON from response")
        print("Raw response:", result.text) 

singleRecipient = [{'Email': 'hudsonkass20@gmail.com'}]

# Main execution
recipients = fetch_recipients()
html_body = generate_html_body(headlines, urls, description, domains)
send_email(html_body, singleRecipient)
