import os
import requests

def verify_email(email):
    try:
        # Ensure you have ABSTRACT_API in your environment variables
        api_key = os.getenv('ABSTRACT_API')
        if not api_key:
            raise ValueError("API key is missing. Make sure the ABSTRACT_API environment variable is set.")

        # Construct the API request URL
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"

        # Send a GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for 4xx/5xx responses

        # Parse the response JSON
        data = response.json()

        # Check if the email is deliverable
        return data.get('deliverability') == 'DELIVERABLE'

    except requests.exceptions.RequestException as e:
        print(f"Error verifying email: {e}")
        return False
