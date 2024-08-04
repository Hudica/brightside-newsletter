import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

def send_email():
    try:
        ses = boto3.client(
            'ses',
            region_name='us-east-1',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )

        response = ses.send_email(
            Source='brightside-news@hudica.info',
            Destination={
                'ToAddresses': [
                    'andrew@kass.net',
                ],
            },
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
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    except NoCredentialsError:
        print("Error: No credentials provided for AWS SES.")
    except PartialCredentialsError:
        print("Error: Incomplete credentials provided.")
    except Exception as e:
        print("Error:", e)

send_email()
