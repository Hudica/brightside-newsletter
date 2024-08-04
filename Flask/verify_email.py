import os
import requests

def verify_email(email):
    try:
        # Ensure you have HUNTER_API_KEY in your environment variables
        api_key = os.getenv('HUNTER_API_KEY')
        url = f"https://api.hunter.io/v2/email-verifier?email={requests.utils.quote(email)}&api_key={api_key}"

        response = requests.get(url)
        response.raise_for_status() 
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error verifying email: {e}")
        return None
