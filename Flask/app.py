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

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/score')
def positivity_score():
    return render_template('positivity_score.html')

@app.route('/subscribe', methods=['POST'])
def add_subscriber():
    try:
        email = request.form.get('email')
        if not email:
            return "No email provided, please enter an email.", 400

        normalized_email = email.lower()

        if subscribers.find_one({"email": normalized_email}):
            return "Email already subscribed. Please use another email.", 409

        if verify_email(email):
            try:
                subscribers.insert_one({"email": normalized_email})
                return "Subscription successful!", 200
            except Exception as db_error:
                print(f"Database Insertion Error: {db_error}")
                return "Internal Server Error", 500
        else:
            return "Please provide a valid email address.", 400

    except Exception as e:
        print(f"Internal Server Error: {e}")
        return "Internal Server Error", 500



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
