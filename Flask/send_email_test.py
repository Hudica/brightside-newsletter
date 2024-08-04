import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from dotenv import load_dotenv
import sqlite3
import pandas as pd

csv_file_path = '../headline_data/used_headlines.csv'

df = pd.read_csv(csv_file_path)

headlines = df['Headline'].tail(3).tolist()

urls = df['URL'].tail(3).tolist()

load_dotenv()

def fetch_recipients():
    conn = sqlite3.connect('instance/subscribers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM subscriber')
    rows = cursor.fetchall()
    emails = [row[0] for row in rows]
    cursor.close()
    conn.close()
    return emails

def send_email(recipients):
    ses = boto3.client(
        'ses',
        region_name='us-east-1',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
    )
    try:
        response = ses.send_email(
        Source='brightside-news@hudica.info',
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
        print(f"Email sent to user! Message ID:", response['MessageId'])
    except NoCredentialsError:
        print("Error: No credentials provided for AWS SES.")
    except PartialCredentialsError:
        print("Error: Incomplete credentials provided.")
    except Exception as e:
        print(f"Error sending to user:", e)

html_body = f"""
<html>
<head>
    <style>
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            margin: 20px;
            color: #333333;
            background-color: #f4f4f9;
            line-height: 1.6;
        }}
        h1 {{
            color: #0066cc;
        }}
        p {{
            font-size: 16px;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
            padding: 10px;
            background-color: #ffffff;
            border: 1px solid #dddddd;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <h1>Welcome to The Brightside Newsletter!</h1>
    <p>Here are the latest updates from positive news worldwide, delivered straight to your inbox:</p>
    <ul>
"""

for headline, url in zip(headlines, urls):
    html_body += f"""        <li>
            <strong><a href="{url}" target="_blank">{headline}</a></strong>
        </li>
"""

html_body += """
    </ul>
    <p>Thank you for subscribing to our newsletter. Stay tuned for more updates!</p>
</body>
</html>
"""



recipients = fetch_recipients()
send_email(recipients)
