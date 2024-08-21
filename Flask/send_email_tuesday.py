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
    background_url = "https://images.unsplash.com/photo-1548614229-c1fe21dfab63?q=80&w=2565&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90oy1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    fallback_color = "#242124"  # Dark grey

    html_body = f"""
    <html>
    <body style="font-family: 'Helvetica', 'Arial', sans-serif; margin: 0; padding: 20px; text-align: center; background-color: {fallback_color}; background-image: url('{background_url}'); background-size: cover; background-position: center;">
        <!--[if gte mso 9]>
        <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
            <v:fill type="tile" src="{background_url}" color="{fallback_color}"/>
        </v:background>
        <![endif]-->
        <h1 style="color: #fcc200; margin-bottom: 20px; font-size: 2.75em;">The Brightside Newsletter!</h1>
        <p style="color: #a9a9a9; font-size: 1.4em; margin-bottom: 20px;">Happy Tuesday! We provide the latest updates from positive and interesting news worldwide, delivered straight to your inbox. These articles were classified to be positive by our custom AI model.</p>
        <table style="width: 100%; max-width: 600px; margin: 0 auto; background-color: rgba(0, 0, 0, 0.8); box-shadow: 0px 0px 10px rgba(0,0,0,0.3);">
    """
    for headline, url, desc, domain in zip(headlines, urls, description, domains):
        html_body += f"""
            <tr>
                <td style="background-color: #fffafa; border: 1px solid #dcdcdc; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
                    <a href="{url}" target="_blank" style="color: #3366cc; text-decoration: none; font-size: 1.5em;">{headline}</a>
                    <p style="font-size: 1em; color: #444444; margin-top: 10px;">{desc}</p>
                    <p style="font-size: 1em; color: #666666; margin-top: 5px;">(Credit: {domain})</p>
                </td>
            </tr>
        """
    html_body += f"""
        </table>
        <p style="color: #696969; font-size: 1.2em;">Thank you for subscribing to our newsletter. Stay tuned for more updates!</p>
        <p style="color: #696969; font-size: 1.2em;">To contact the newsletter with any questions or concerns, please reach out <a href="mailto:brightside-news@hudica.info" style="color: #3366cc;">here</a>.</p>
        <div style="color: #696969; text-align: center; padding: 20px; font-size: 0.9em; border-top: 1px solid #444;">
            <p>To unsubscribe from our newsletter, please <a href="https://news.hudica.info/unsubscribe" style="color: #3366cc; text-decoration: none;">click here</a>.</p>
        </div>
    </body>
    </html>
    """
    return html_body



def send_email(html_body, recipients):
    data = {
        'FromEmail': "brightside-news@hudica.info",
        'FromName': "Brightside Newsletter",
        'Recipients': recipients,
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


# Main execution
recipients = fetch_recipients()
html_body = generate_html_body(headlines, urls, description)
send_email(html_body, recipients)
