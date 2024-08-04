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
                Destination={'ToAddresses': [recipient]}, 
                Message={
                    'Subject': {
                        'Data': 'Test email from Amazon SES',
                    },
                    'Body': {
                        'Text': {
                            'Data': 'Hello, this is a test email sent by Amazon SES!',
                        },
                    },
                }
            )
            print(f"Email sent to {recipient}! Message ID:", response['MessageId'])
        except NoCredentialsError:
            print("Error: No credentials provided for AWS SES.")
        except PartialCredentialsError:
            print("Error: Incomplete credentials provided.")
        except Exception as e:
            print(f"Error sending to {recipient}:", e)

#recipients = fetch_recipients()
#send_email(recipients)
