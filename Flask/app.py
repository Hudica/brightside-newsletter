from flask import Flask, render_template, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from Flask.verify_email import verify_email

app = Flask(__name__)
load_dotenv()

mongo_conn_string = os.getenv('MONGO_CONN_STRING')
client = MongoClient(mongo_conn_string)
db = client.BrightSideUsers
subscribers = db.emails

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/unsubscribe')
def unsubscribe():
    return render_template('unsubscribe.html')

@app.route('/subscribe', methods=['POST'])
def add_subscriber():
    email = request.form.get('email')
    if not email:
        return "No email provided, please enter an email.", 400
    
    normalized_email = email.lower() 
    
    if subscribers.find_one({"email": normalized_email}):
        return "Email already subscribed. Please use another email.", 409
    
    verification_result = verify_email(email)
    if verification_result and verification_result['data']['status'] == 'valid':
        try:
            subscribers.insert_one({"email": normalized_email})
            return "Subscription successful!", 200
        except Exception as e:
            print(str(e))
            return "Error processing your subscription.", 500
    else:
        return "Please provide a valid email address.", 400

@app.route('/unsubscribeAction', methods=['POST'])
def unsubscribeAction():
    email = request.form.get('email')
    if not email:
        return "No email provided, please enter an email.", 400
    
    normalized_email = email.lower() 
    
    if subscribers.delete_one({"email": normalized_email}).deleted_count > 0:
        return "You have been successfully unsubscribed.", 200
    else:
        return "Email not found in our database.", 404

if __name__ == "__main__":
    app.run(debug=True)
