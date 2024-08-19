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
    <head>
        <style>
            body {
                font-family: 'Helvetica', 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                color: #f0f0f0;
                background-color: #1e1e1e;
                background: linear-gradient(to right, #3a3a3a, #1e1e1e);
                text-align: center;
                box-sizing: border-box;
            }
            h1 {
                color: #ffd700;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            p {
                font-size: 1.2em;
                color: #dcdcdc;
                margin-bottom: 20px;
            }
            a {
                color: #ffd700;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            ul {
                list-style-type: none;
                padding: 0;
                max-width: 90%;
                margin: 0 auto;
            }
            li {
                margin: 20px 0;
                padding: 20px;
                background-color: #2e2e2e;
                border: 2px solid #444444;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                text-align: left;
            }
            li strong {
                font-size: 1.5em;
                display: block;
                margin-bottom: 10px;
                color: #ffd700;
            }
            li p {
                margin-top: 10px;
                font-size: 1em;
                color: #dcdcdc;
            }
            @media (max-width: 600px) {
                body {
                    padding: 10px;
                }
                h1 {
                    font-size: 2em;
                }
                p {
                    font-size: 1em;
                }
                li {
                    padding: 15px;
                }
                li strong {
                    font-size: 1.2em;
                }
                li p {
                    font-size: 0.9em;
                }
            }
        </style>
    </head>
    <body>
        <h1>Welcome to The Brightside Newsletter!</h1>
        <p>Here are the latest updates from positive news worldwide, delivered straight to your inbox.</p>
        <ul>
    """
    for headline, url, desc in zip(headlines, urls, description):
        html_body += f"""
            <li>
                <strong><a href='{url}' target='_blank'>{headline}</a></strong>
                <p>{desc}</p>
            </li>
        """
    html_body += """
        </ul>
    </body>
    </html>
    """
    return html_body

def send_email(html_body, recipients):
    data = {
        'FromEmail': "brightside-news@hudica.info",
        'FromName': "Brightside Newsletter",
        'Recipients': recipients,
        'Subject': "Brightside News - Latest Updates",
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

singleRecipient = [{'Email': 'hudson@kass.net'}]

# Main execution
recipients = fetch_recipients()
html_body = generate_html_body(headlines, urls, description)
send_email(html_body, recipients)
