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
score = df['Score'].tail(1).values[0] * 100
print(score)

# Set up MongoDB connection
mongo_conn_string = os.getenv('MONGO_CONN_STRING')
client = MongoClient(mongo_conn_string)
db = client.BrightSideUsers
subscribers_collection = db.emails

def get_color(score):
    if score <= 10:
        return "#c62828"  # Strong Red
    elif score <= 13:
        return "#d32f2f"  # Deep Red
    elif score <= 16:
        return "#ef6c00"  # Deep Orange
    elif score <= 19:
        return "#f57c00"  # Pumpkin Orange
    elif score <= 22:
        return "#f9a825"  # Saffron
    elif score <= 25:
        return "#fbc02d"  # Bright Yellow
    elif score <= 28:
        return "#9ccc65"  # Light Green
    elif score <= 31:
        return "#7cb342"  # Olive Green
    elif score <= 34:
        return "#558b2f"  # Dark Lime Green
    else:
        return "#33691e"  # Dark Green
color = get_color(score)

def fetch_recipients():
    emails = [{'Email': doc['email']} for doc in subscribers_collection.find({}, {"_id": 0, "email": 1})]
    return emails
def generate_html_body(headlines, urls, description, domains):
    # HTML body of the email with creative and enhanced visual elements
    html_body = f"""
    <html>
    <body style="font-family: 'Helvetica', 'Arial', sans-serif; margin: 0 auto; padding: 20px; text-align: center; max-width: 1000px;">
        <h1 style="color: #DAA520; margin-bottom: 30px; font-size: 2.5em; border-bottom: 3px solid #DAA520;">
            <a href="http://news.hudica.info" target="_blank" style="color: #DAA520; text-decoration: none;">The Brightside Newsletter</a>
        </h1>

        <!-- Positivity Score -->
        <section style="padding: 10px; margin-bottom: 10px;">
            <h2 style="color: #333333; font-size: 1.75em; margin-bottom: 4px;"><u>Positivity Score</u></h2>
            <p style="font-size: 3em; color: {color}; margin-top: 0px; margin-bottom: 2px;">{score}%</p>
            <p style="font-size: 0.8em; margin-top: 0px; margin-bottom: 4px;">
                This score represents the percentage of positive headlines out of the total headlines analyzed.
            </p>
            <p style="margin-bottom: 30px;"><a href="https://news.hudica.info/score" style="color: #275af4; font-size: 0.8em; text-decoration: none;">How it's calculated</a></p>
        </section>



        <!-- Featured Headlines -->
        <section style="padding: 20px; background-color: #E8E8E8; margin-bottom: 20px;">
            <h2 style="color: #333333; font-size: 1.5em; border-bottom: 1px dashed #B8860B; margin-bottom: 20px;">Featured Headlines</h2>
    """
    for headline, url, desc, domain in zip(headlines, urls, description, domains):
        html_body += f"""
            <div style="background-color: #FFFFFF; padding: 15px; margin-bottom: 15px; border-left: 5px solid #DAA520; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
                <a href="{url}" target="_blank" style="color: #3366CC; text-decoration: none; font-size: 1.25em;"><strong>{headline}</strong></a>
                <p style="font-size: 1em; color: #444444; margin-top: 10px;">{desc}</p>
                <p style="font-size: 0.7em; color: #666666; margin-top: 5px;">(Credit: <a href="{url}" target="_blank" style="color: #3366CC; text-decoration: none;">{domain}</a>)</p>
            </div>
        """
    html_body += f"""
        </section>

        <!-- Mission Statement Section -->
        <section style="padding: 20px; background-color: #FFFFFF; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); margin-bottom: 20px;">
            <h2 style="color: #333333; font-size: 1.5em; margin-bottom: 10px;"><u>The Mission</u></h2>
            <p style="font-size: 0.95em; color: #333333;">In a world often overshadowed by negative news, our mission is to shine a light on the good. We scan the web for stories of hope, progress, and unity, bringing you a curated selection of positive news that inspires and uplifts. This newsletter is completely free and only exists to make people smile!</p>
        </section>

        <!-- How It Works Section -->
        <section style="padding: 20px; background-color: #F4F4F4; margin-bottom: 20px;">
            <h2 style="color: #333333; font-size: 1.5em; margin-bottom: 10px;"><u>How It Works</u></h2>
            <p style="font-size: 0.95em; color: #333333;">This newsletter uses a complex sentiment analysis model to identify the most positive and interesting headlines from established news outlets. This allows us to present you with news that not only informs but also contributes to a more optimistic worldview.</p>
        </section>

        <hr style="border: 0; height: 1px; background-color: #CCCCCC; margin-bottom: 20px; margin-top: 50px;">

        <!-- Footer Section -->
        <!-- Footer Section -->
        <footer style="padding: 30px; background-color: #F3F3F3; text-align: center; color: #333333; font-size: 1em; border-top: 2px solid #CCCCCC;">
            <p style="margin-bottom: 15px;">Thank you for subscribing to The Brightside Newsletter. Stay tuned for more updates and positivity!</p>
            <p style="margin-bottom: 15px;">Did you find this email enjoyable? Forward it to a friend!</p>
            <p style="margin-bottom: 10px;">Was this email forwarded to you? Subscribe <a href="https://news.hudica.info" style="color: #3366CC; text-decoration: none;">here</a></p>
            
            <!-- Separator Line -->
            <hr style="border: 0; height: 1px; background-color: #CCCCCC; margin-bottom: 20px;">

            <p style="margin-bottom: 20px; font-size: 0.9em;">Questions or feedback? Reach out <a href="mailto:brightside-news@hudica.info" style="color: #3366CC; text-decoration: none;">here</a></p>
            <p style="font-size: 0.8em; color: #666666;">Want to unsubscribe? <a href="https://news.hudica.info/unsubscribe" style="color: #3366CC; text-decoration: none;">Click here</a></p>
            <p style="font-size: 0.8em; color: #666666;">For information about our privacy practices, see our <a href="https://news.hudica.info/unsubscribe" style="color: #3366CC; text-decoration: none;">Privacy Statement</a>.</p>
        </footer>

    </body>
    </html>
    """
    return html_body



def send_email(html_body, recipients):
    data = {
        'FromEmail': "brightside-news@hudica.info",
        'FromName': "Brightside Newsletter",
        'Recipients': recipients,
        'Subject': "Brightside News, Tuesday Edition!",
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

single = [{'Email': 'hudson@kass.net'}]

# Main execution
recipients = fetch_recipients()
html_body = generate_html_body(headlines, urls, description, domains)
send_email(html_body, recipients)
