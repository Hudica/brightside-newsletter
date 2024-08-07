import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient

csv_file_path = './headline_data/used_headlines.csv'

df = pd.read_csv(csv_file_path)

headlines = df['Headline'].tail(4).tolist()
urls = df['URL'].tail(3).tolist()
description = df['Description'].tail(4).tolist()

load_dotenv()

# Set up MongoDB connection
mongo_conn_string = os.getenv('MONGO_CONN_STRING')
client = MongoClient(mongo_conn_string)
db = client.BrightSideUsers
subscribers_collection = db.emails

def fetch_recipients():
    emails = [doc['email'] for doc in subscribers_collection.find({}, {"_id": 0, "email": 1})]
    return emails

def send_email(recipients):
    ses = boto3.client(
        'ses',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
    )
    for i in range(1):
        try:
            response = ses.send_email(
                Source='BrightSide Newsletter <brightside-news@hudica.info>',
                Destination={
                    'ToAddresses': ['hudson@kass.net']
                },
                Message={
                    'Subject': {
                        'Data': 'Brightside News - Latest Updates'
                    },
                    'Body': {
                        'Html': {
                            'Data': html_body
                        }
                    }
                }
            )
            print(f"Email sent to hudson! Message ID:", response['MessageId'])
        except NoCredentialsError:
            print("Error: No credentials provided for AWS SES.")
        except PartialCredentialsError:
            print("Error: Incomplete credentials provided.")
        except Exception as e:
            print(f"Error sending to hudson:", e)

html_body = f"""
<html>
<head>
    <style>
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            color: #f0f0f0;
            background-color: #1e1e1e;
            background: linear-gradient(to right, #3a3a3a, #1e1e1e);
            text-align: center;
            box-sizing: border-box;
        }}
        h1 {{
            color: #ffd700;
            margin-bottom: 20px;
            font-size: 2.5em;
        }}
        p {{
            font-size: 1.2em;
            color: #dcdcdc;
            margin-bottom: 20px;
        }}
        a {{
            color: #ffd700;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
            max-width: 90%;
            margin: 0 auto;
        }}
        li {{
            margin: 20px 0;
            padding: 20px;
            background-color: #2e2e2e;
            border: 2px solid #444444;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: left;
        }}
        li strong {{
            font-size: 1.5em;
            display: block;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        li p {{
            margin-top: 10px;
            font-size: 1em;
            color: #dcdcdc;
        }}
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 2em;
            }}
            p {{
                font-size: 1em;
            }}
            li {{
                padding: 15px;
            }}
            li strong {{
                font-size: 1.2em;
            }}
            li p {{
                font-size: 0.9em;
            }}
        }}
    </style>
</head>
<body style="background-color: #1e1e1e; background: linear-gradient(to right, #3a3a3a, #1e1e1e); color: #f0f0f0; text-align: center; box-sizing: border-box;">
    <h1 style="color: #ffd700; margin-bottom: 20px; font-size: 2.5em;">Welcome to The Brightside Newsletter!</h1>
    <p style="font-size: 1.2em; color: #dcdcdc; margin-bottom: 20px;">
        Here are the latest updates from positive news worldwide, delivered straight to your inbox:
    </p>
    <ul style="list-style-type: none; padding: 0; max-width: 90%; margin: 0 auto;">
"""

for headline, url, desc in zip(headlines, urls, description):
    html_body += f"""        <li style="margin: 20px 0; padding: 20px; background-color: #2e2e2e; border: 2px solid #444444; border-radius: 12px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); text-align: left;">
            <strong style="font-size: 1.5em; display: block; margin-bottom: 10px; color: #ffd700;"><a href="{url}" target="_blank" style="color: #ffd700; text-decoration: none;">{headline}</a></strong>
            <p style="margin-top: 10px; font-size: 1em; color: #dcdcdc;">{desc}</p>
        </li>
"""

html_body += """
    </ul>
    <p style="font-size: 1.2em; color: #dcdcdc; margin-bottom: 20px;">
        Thank you for subscribing to our newsletter. Stay tuned for more updates!
    </p>
    <p style="font-size: 1.2em; color: #dcdcdc; margin-bottom: 20px;">
        To contact the newsletter with any questions or concerns, please reach out at <a href="mailto:brightside-news@hudica.info" style="color: #ffd700; text-decoration: none;"> this email</a>.
    </p>
    <p style="font-size: 1.2em; color: #dcdcdc; margin-bottom: 20px;">
        To unsubscribe from our newsletter, please click <a href="http://news.hudica.info/unsubscribe" style="color: #ffd700; text-decoration: none;">here</a>.
    </p>
</body>
</html>
"""


recipients = fetch_recipients()
send_email(recipients)
