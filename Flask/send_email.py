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

description = df['Description'].tail(3).tolist()

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
            margin: 0;
            padding: 20px;
            color: #333333;
            background: linear-gradient(to right, #f6d365, #fda085); /* Simplified gradient */
            background: -webkit-linear-gradient(to right, #f6d365, #fda085); /* For Safari 5.1 to 6.0 */
            background: -moz-linear-gradient(to right, #f6d365, #fda085); /* For Firefox 3.6 to 15 */
            background: -o-linear-gradient(to right, #f6d365, #fda085); /* For Opera 11.1 to 12.0 */
            background: -ms-linear-gradient(to right, #f6d365, #fda085); /* For Internet Explorer 10 */
            line-height: 1.6;
            text-align: center;
            box-sizing: border-box; /* Ensures padding doesn't break layout */
        }}
        h1 {{
            color: #ff6347;
            margin-bottom: 20px;
            font-size: 2em; /* Responsive font size */
        }}
        p {{
            font-size: 1.2em; /* Responsive font size */
            color: #2c3e50;
            margin-bottom: 20px;
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
            max-width: 90%; /* Responsive width */
            margin: 0 auto;
        }}
        li {{
            margin: 20px 0;
            padding: 20px;
            background-color: #ffffff;
            border: 2px solid #dddddd;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            text-align: center; /* Center align for list items */
        }}
        li strong {{
            font-size: 1.5em; /* Responsive font size */
            display: block;
            margin-bottom: 10px;
        }}
        li p {{
            margin-top: 10px;
            font-size: 1em; /* Responsive font size */
            color: #555555;
        }}
        @media (max-width: 600px) {{
            body {{
                padding: 10px;
            }}
            h1 {{
                font-size: 1.5em;
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
<body>
    <h1>Welcome to The Brightside Newsletter!</h1>
    <p>Here are the latest updates from positive news worldwide, delivered straight to your inbox:</p>
    <ul>
"""

for headline, url, desc in zip(headlines, urls, description):
    html_body += f"""        <li>
            <strong><a href="{url}" target="_blank">{headline}</a></strong>
            <p>{desc}</p>
        </li>
"""

html_body += """
    </ul>
    <p>Thank you for subscribing to our newsletter. Stay tuned for more updates!</p>
    <p>To unsubscribe from our newsletter, please click <a href="http://yourdomain.com/unsubscribe">here</a>.</p>
</body>
</html>
"""





recipients = fetch_recipients()
send_email(recipients)
