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

desc = df['Description'].tail(3).tolist()

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
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            color: #4A4A4A;
            background-color: #F9F9F9;
            line-height: 1.6;
            text-align: center;
        }}
        h1 {{
            color: #3498db;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 18px;
            color: #666666;
        }}
        a {{
            color: #e67e22;
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
            background-color: #ffffff;
            margin: 10px auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 90%;
            max-width: 800px;
            text-align: left;
        }}
        .description {{
            font-size: 16px;
            color: #333;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>Welcome to The Brightside Newsletter!</h1>
    <p>Here are the latest updates from positive news worldwide, delivered straight to your inbox:</p>
    <ul>
"""

for headline, url, desc in zip(headlines, urls, desc):  # Ensure descriptions is your list of descriptions
    html_body += f"""        <li>
            <strong><a href="{url}" target="_blank">{headline}</a></strong>
            <p class='description'>{desc}</p>  <!-- Description added below the headline -->
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
