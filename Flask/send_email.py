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
    for recipient in recipients:
        try:
            response = ses.send_email(
            Source='brightside-news@hudica.info',
            Destination={
                'ToAddresses': [recipient]
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
            print(f"Email sent to {recipient}! Message ID:", response['MessageId'])
        except NoCredentialsError:
            print("Error: No credentials provided for AWS SES.")
        except PartialCredentialsError:
            print("Error: Incomplete credentials provided.")
        except Exception as e:
            print(f"Error sending to {recipient}:", e)

html_body = f"""
<html>
<head>
    <style>
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            margin: 20px;
            color: #35495E;  # Updated to a darker, richer blue for better readability
            background-color: #F7F7F7;  # A softer, lighter grey to keep it light and modern
            line-height: 1.6;
        }}
        h1 {{
            color: #D35400;  # A strong, assertive orange for headings to capture attention
        }}
        p {{
            font-size: 16px;
            color: #2C3E50;  # Deep blue for body text provides a calm, professional tone
        }}
        a {{
            color: #2980B9;  # Bright blue for links to stand out nicely
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
            color: #3498DB;  # Lighter shade of blue on hover for a pleasant visual effect
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
            padding: 10px;
            background-color: #ECF0F1;  # Very light gray background in list items for subtle contrast
            border: 1px solid #BDC3C7;  # Border color for list items
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

html_body += f"""
    </ul>
    <p>Thank you for subscribing to our newsletter. Stay tuned for more updates!</p>
    <p>To unsubscribe from our newsletter, please click <a href="http://yourdomain.com/unsubscribe">here</a>.</p>
</body>
</html>
"""





recipients = fetch_recipients()
send_email(recipients)
