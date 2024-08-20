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
def generate_html_body(headlines, urls, description):
    html_body = """
    <html>
    <body style="font-family: 'Helvetica', 'Arial', sans-serif; margin: 0; padding: 20px; color: #f0f0f0; background-color: #1e1e1e; background: linear-gradient(to right, #3a3a3a, #1e1e1e); text-align: center;">
        <h1 style="color: #ffd700; margin-bottom: 20px; font-size: 2.5em;">Here is The Brightside Newsletter!</h1>
        <p style="font-size: 1.2em; color: #dcdcdc; margin-bottom: 20px;">We provide the latest updates from positive and interesting news worldwide, delivered straight to your inbox. These articles were classified to be positive by our custom AI model.</p>
        <table style="width: 100%; max-width: 600px; margin: 0 auto;">
    """
    for headline, url, desc, domain in zip(headlines, urls, description, domains):
        html_body += f"""
            <tr>
                <td style="background-color: #2e2e2e; border: 2px solid #444; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
                    <a href="{url}" target="_blank" style="color: #ffd700; text-decoration: none; font-size: 1.5em;">{headline}</a>
                    <p style="font-size: 1em; color: #fff5ee; margin-top: 10px;">{desc}</p>
                    <p style = "font-size: 1em; color: #dcdcdc; margin-top 5px;">(Credit: {domain})</p>
                </td>
            </tr>
        """
    html_body += """
        </table>
        <p style="font-size: 1.2em; color: #dcdcdc;">Thank you for subscribing to our newsletter. Stay tuned for more updates!</p>
        <p style="font-size: 1.2em; color: #dcdcdc;">To contact the newsletter with any questions or concerns, please reach out at <a href="mailto:brightside-news@hudica.info" style="color: #ffd700;">this email</a>.</p>
        <p style="font-size: 1.2em; color: #dcdcdc;">To unsubscribe from our newsletter, please click <a href="https://news.hudica.info/unsubscribe" style="color: #ffd700; text-decoration: none;"><u>here.</u></a></p>
    </body>
    </html>
    """
    return html_body



def send_email(html_body, recipients):
    data = {
        'FromEmail': "brightside-news@hudica.info",
        'FromName': "Brightside Newsletter",
        'Recipients': recipients,
        'Subject': "Brightside News Thursday Edition!",
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


# Main execution
recipients = fetch_recipients()
html_body = generate_html_body(headlines, urls, description)
send_email(html_body, recipients)
